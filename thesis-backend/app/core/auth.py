from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from typing import Optional
from app.models.user import User
from app.models.staff import Staff
from app.models.patient import Patient
from app.schemas.user import TokenData
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from app.db.session import get_session

# Secret and algorithm (store secret in .env later)
SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str, session: Session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = session.exec(select(User).where(User.username == username)).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> User:
    return verify_token(token, session)

def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admins only"
        )
    return current_user

def get_current_patient(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> Patient:
    if current_user.role != "patient":
        raise HTTPException(status_code=403, detail="Patients only")

    patient = session.exec(select(Patient).where(Patient.user_id == current_user.id)).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient record not found")

    return patient


def get_current_admin_or_hr(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in ("admin", "hr"):
        raise HTTPException(
            status_code=403,
            detail="Only admins and HR can access this"
        )
    return current_user

def get_current_admin_or_lab_tech(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> User:
    if current_user.role == "admin":
        return current_user

    if current_user.role == "staff":
        statement = select(Staff).where(
            Staff.user_id == current_user.id,
            Staff.role == "lab_technician"
        )
        staff_member = session.exec(statement).first()

        if staff_member:
            return current_user

    raise HTTPException(
        status_code=403,
        detail="Only admins and lab technicians can view lab tests"
    )

def get_current_airflow(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "airflow":
        raise HTTPException(
            status_code=403,
            detail="Airflow-only access"
        )
    return current_user



