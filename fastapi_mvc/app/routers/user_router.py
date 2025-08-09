from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.controllers import user_controller
from app.utils.jwt_auth import get_current_user
from fastapi import Query

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





