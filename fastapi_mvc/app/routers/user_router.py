from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.controllers import user_controller
from app.utils.jwt_auth import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/createUser")
async def register_user(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return user_controller.create_user(db, data)

@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    return  user_controller.login_user(db, data)

@router.get("/protected-route")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Welcome {current_user['userId']}! This is a protected route."}


