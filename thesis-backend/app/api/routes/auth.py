from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.user import User
from app.core.security import verify_password
from app.core.auth import create_access_token, oauth2_scheme, get_current_user
from app.schemas.user import Token, UserRead, TokenWithUser
from datetime import timedelta

router = APIRouter()

@router.post("/login", response_model=TokenWithUser)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    user = session.exec(select(User).where(User.username == form_data.username)).first()


    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.role == "airflow":
        access_token_expires = timedelta(days=365)
    else:
        access_token_expires = timedelta(minutes=30)

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires

    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }
@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


