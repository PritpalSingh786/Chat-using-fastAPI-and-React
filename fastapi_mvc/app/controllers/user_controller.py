from app.models.user import CustomUser, Post, Notification
from app.models.message import Message
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import bcrypt
from app.utils.jwt_handler import create_access_token
from datetime import timedelta, datetime
from zoneinfo import ZoneInfo
from app.socket_manager import send_notification_to_invitedUsers
import asyncio
from sqlalchemy import func, text
from sqlalchemy.dialects.postgresql import JSONB  # If using PostgreSQL
from sqlalchemy.sql.expression import cast
from sqlalchemy.types import JSON


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
    
    # 4. Mark user as logged in
    user.isLogin = True
    db.commit()
    db.refresh(user)

    # 5. Return user (or generate token if needed)
    access_token = create_access_token(data={
        "userId": user.userId,
        "id": user.id,
        "email": user.email,
        "iat": int(datetime.utcnow().timestamp())
    },
    # expires_delta=timedelta(minutes=60)
    )
    return {
        "message": "Login successful",
        "userId": user.userId,
        "email": user.email,
        "id": user.id,
        "token": access_token,
    }

def logout_user(db: Session, current_user_id: int):
    user = db.query(CustomUser).filter(CustomUser.id == current_user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Mark as logged out
    user.isLogin = False
    db.commit()
    db.refresh(user)

    return {
        "message": "Logout successful",
        "userId": user.userId,
        "isLogin": user.isLogin
    }

def get_all_users_except_current(db: Session, current_user_id: int, page: int, per_page: int):
    query = db.query(CustomUser).filter(CustomUser.id != current_user_id).order_by(CustomUser.createdAt.desc())
    print(query, "qqqq")
    total = query.count()
    users = query.offset((page - 1) * per_page).limit(per_page).all()

    user_list = [{
        "id": user.id,
        "userId": user.userId,
        "email": user.email,
    } for user in users]

    return {
        "total": total,
        "page": page,
        "perPage": per_page,
        "users": user_list,
    }

def messages(db: Session, user_data: dict):
    print(user_data,"userdddddd")
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request body cannot be empty. senderId and receiverId are required."
        )
    # Manual validation for required keys
    if "senderId" not in user_data or "receiverId" not in user_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Both senderId and receiverId are required."
        )
    
    messages = (
        db.query(Message)
        .filter(
            Message.sender_id.in_([user_data["senderId"], user_data["receiverId"]]),
            Message.receiver_id.in_([user_data["senderId"], user_data["receiverId"]])
        )
        .order_by(Message.createdAt)
        .all()
    )
    result = [
    {
        "senderId": msg.sender_id,
        "receiverId": msg.receiver_id,
        "message": msg.message,
        "createdAt": msg.createdAt.replace(
            tzinfo=ZoneInfo("UTC")
        ).astimezone(
            ZoneInfo("Asia/Kolkata")
        ).strftime("%Y-%m-%d %H:%M:%S")
    }
    for msg in messages
    ]
    return result

def createPost(db: Session, data: dict):
    # Validate required fields
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request body cannot be empty"
        )
    if 'postTitle' not in data or not data['postTitle']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post title is required"
        )
    
    if 'invited_ids' not in data or not data['invited_ids']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invited IDs are required"
        )
    
    # Validate invited_ids is a list
    if not isinstance(data['invited_ids'], list):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invited IDs must be provided as a list"
        )
    
    current_id = data['id']
    print(current_id)
    title = data['postTitle']
    invited_ids = data['invited_ids']
    
    # Validate not inviting yourself
    if current_id in invited_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot invite yourself"
        )
    
    # Validate maximum invited users
    if len(invited_ids) > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 5 users can be invited"
        )
    
    # Verify all invited users exist
    existing_ids = {user.id for user in db.query(CustomUser.id).filter(CustomUser.id.in_(invited_ids)).all()}
    invalid_ids = set(invited_ids) - existing_ids
    if invalid_ids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid user IDs: {invalid_ids}"
        )
    
    # Create the post
    try:
        post = Post(
            postTitle=title,
            invited_user_ids=invited_ids
        )
        db.add(post)
        db.commit()
        db.refresh(post)
        message = f"User {data['userId']} invited you to join '{title}'"
        notification = Notification(
            notifyTextMessage=message,
            invited_user_ids=invited_ids
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        print(post, "posttttt")
        notification_data = {
            "message": message,
        }
        asyncio.create_task(send_notification_to_invitedUsers(
            user_ids=invited_ids,
            event_name='send_notification_to_invitedUsers',
            data=notification_data
            ))
        return {
            "status": "success",
            "message": "Post created successfully",
            "data": post
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Post creation failed: {str(e)}"
        )

def get_notifications(db: Session, current_user_id: int, page: int, per_page: int):
    # JSON_CONTAINS(invited_user_ids, 'current_user_id') requires the value as JSON string
    current_user_json = f'"{current_user_id}"'  # wrap the id in double quotes to match JSON string

    query = db.query(Notification).filter(
        func.JSON_CONTAINS(Notification.invited_user_ids, current_user_json)
    ).order_by(Notification.createdAt.desc())

    total = query.count()
    notifications = query.offset((page - 1) * per_page).limit(per_page).all()

    notification_list = [{
        "id": n.id,
        "notifyTextMessage": n.notifyTextMessage,
        "invited_user_ids": n.invited_user_ids,
        "createdAt": n.createdAt.isoformat() if n.createdAt else None,
    } for n in notifications]

    return {
        "total": total,
        "page": page,
        "perPage": per_page,
        "notifications": notification_list,
    }