from typing import List

from sqlmodel import Session, select
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password
from fastapi import HTTPException, status

def create_user(user_in: UserCreate, session: Session) -> User:
    statement = select(User).where(User.username == user_in.username)
    existing_user = session.exec(statement).first()


    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    # Check if email exists
    statement = select(User).where(User.email == user_in.email)
    existing_email = session.exec(statement).first()

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    user = User(
        username=user_in.username,
        email=user_in.email,
        password=hash_password(user_in.password),
        role=user_in.role,
        contact_info=user_in.contact_info,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_users(session: Session) -> List[User]:
    return session.exec(select(User)).all()
