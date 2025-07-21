from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from app.schemas.staff import StaffCreate, StaffRead, StaffUpdate
from app.crud.staff import create_staff, get_staff , update_staff
from app.db.session import get_session
from app.core.auth import get_current_admin, get_current_user
from app.models.user import User
from app.models.staff import Staff


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

@router.get("/me", response_model=StaffRead)
def get_my_staff_profile(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "staff":
        raise HTTPException(status_code=403, detail="Staff only")

    staff = session.exec(select(Staff).where(Staff.user_id == current_user.id)).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff profile not found")

    return staff


@router.put("/{id}", response_model=StaffRead)
def update(
    id: int,
    staff_in: StaffUpdate,
    session: Session = Depends(get_session),
    current_admin: User = Depends(get_current_admin)
):
    return update_staff(id, staff_in, session)

