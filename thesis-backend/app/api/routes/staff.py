from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List

from app.schemas.staff import StaffCreate, StaffRead, StaffUpdate
from app.crud.staff import create_staff, get_staff , update_staff
from app.db.session import get_session
from app.core.auth import get_current_admin, get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=StaffRead, status_code=201)
def create(
    staff_in: StaffCreate,
    session: Session = Depends(get_session),
    current_admin: User = Depends(get_current_admin)
):
    return create_staff(staff_in, session)

@router.get("/", response_model=List[StaffRead])
def list_staff(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return get_staff(session)

@router.put("/{id}", response_model=StaffRead)
def update(
    id: int,
    staff_in: StaffUpdate,
    session: Session = Depends(get_session),
    current_admin: User = Depends(get_current_admin)
):
    return update_staff(id, staff_in, session)

