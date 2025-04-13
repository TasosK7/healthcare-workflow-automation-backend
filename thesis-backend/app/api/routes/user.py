from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.schemas.user import UserCreate, UserRead
from app.models.user import User
from app.crud.user import create_user, get_users
from app.db.session import get_session
from app.core.auth import get_current_admin
from typing import List

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register_user(user_in: UserCreate, session: Session = Depends(get_session)):
    user = create_user(user_in, session)
    return user

@router.get("/", response_model=List[UserRead])
def list_users(
    session: Session = Depends(get_session),
    current_admin: User = Depends(get_current_admin)
):
    return get_users(session)