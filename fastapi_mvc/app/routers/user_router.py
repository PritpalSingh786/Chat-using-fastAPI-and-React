from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.controllers import user_controller
from app.utils.jwt_auth import get_current_user
from fastapi import Query

router = APIRouter()
from pydantic import BaseModel
from typing import List

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

@router.get("/logout")
async def list_all_users(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return user_controller.logout_user(db, current_user["id"])

@router.get("/protected-route")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Welcome {current_user['userId']}! This is a protected route."}

@router.get("/users")
async def list_all_users(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    page: int = Query(1, ge=1),
    perPage: int = Query(10, alias="perPage", ge=1)
):
    return user_controller.get_all_users_except_current(db, current_user["id"], page, perPage)

@router.get("/messages")
async def messages(senderId: str, receiverId: str, db: Session = Depends(get_db), 
                        current_user: dict = Depends(get_current_user),):
      return user_controller.messages(db, {"senderId": senderId, "receiverId": receiverId})

class CreatePostRequest(BaseModel):
    postTitle: str
    invited_ids: List[str]


@router.post("/createPost")
async def createPost(post_data: CreatePostRequest, db: Session = Depends(get_db), 
                     current_user: dict = Depends(get_current_user),):
    data = post_data.dict()
    data['id'] = current_user['id']
    data['userId'] = current_user['userId']
    return user_controller.createPost(db, data)

@router.get("/notifications")
async def get_notifications(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    page: int = Query(1, ge=1),
    perPage: int = Query(10, alias="perPage", ge=1)
):
    return user_controller.get_notifications(db, current_user["id"], page, perPage)






