from app.models.user import CustomUser
from sqlalchemy.orm import Session
from fastapi import HTTPException
import bcrypt
from app.utils.jwt_handler import create_access_token
from datetime import timedelta, datetime


def create_user(db: Session, user_data: dict):
    required_fields = ["userId", "email", "password"]

    # 1. Check for missing or empty fields
    missing_fields = [field for field in required_fields if not user_data.get(field)]
    if missing_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required fields: {', '.join(missing_fields)}"
        )

    # 2. Check if userId or email already exists
    existing_user = db.query(CustomUser).filter(
        (CustomUser.userId == user_data["userId"]) |
        (CustomUser.email == user_data["email"])
    ).first()

    if existing_user:
        if existing_user.userId == user_data["userId"]:
            raise HTTPException(status_code=400, detail="User ID already exists")
        if existing_user.email == user_data["email"]:
            raise HTTPException(status_code=400, detail="Email already exists")

    # 3. Hash the password
    hashed_password = bcrypt.hashpw(user_data["password"].encode("utf-8"), bcrypt.gensalt())

    # 4. Create and save user
    user = CustomUser(
        userId=user_data["userId"],
        email=user_data["email"],
        password=hashed_password.decode("utf-8")
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return {
        "message": "Registered successful"
    }


def login_user(db: Session, user_data: dict):
    required_fields = ["userId", "password"]

    # 1. Check for missing fields
    missing_fields = [field for field in required_fields if not user_data.get(field)]
    if missing_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required fields: {', '.join(missing_fields)}"
        )

    # 2. Find user by userId
    user = db.query(CustomUser).filter(CustomUser.userId == user_data["userId"]).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid userId or password")

    # 3. Check password
    if not bcrypt.checkpw(user_data["password"].encode("utf-8"), user.password.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Invalid userId or password")

    # 4. Return user (or generate token if needed)
    access_token = create_access_token(data={
        "userId": user.userId,
        "id": user.id,
        "email": user.email,
        "iat": int(datetime.utcnow().timestamp())
    },
    expires_delta=timedelta(minutes=60)
    )
    return {
        "message": "Login successful",
        "userId": user.userId,
        "email": user.email,
        "id": user.id,
        "token": access_token,
    }
