from typing import List

from fastapi import HTTPException, status
from app.models.user import User
from app.models.staff import Staff
from app.schemas.staff import StaffCreate
from sqlmodel import Session, select

ALLOWED_STAFF_ROLES = {"staff", "hr", "admin"}

def create_staff(staff_in: StaffCreate, session: Session) -> Staff:
    user = session.get(User, staff_in.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user.role not in ALLOWED_STAFF_ROLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not have a staff-compatible role"
        )

    staff = Staff(**staff_in.model_dump(), email=user.email)
    session.add(staff)
    session.commit()
    session.refresh(staff)
    return staff

def get_staff(session: Session) -> List[Staff]:
    return session.exec(select(Staff)).all()

from app.schemas.staff import StaffUpdate

def update_staff(id: int, staff_in: StaffUpdate, session: Session) -> Staff:
    staff = session.get(Staff, id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")

    for key, value in staff_in.model_dump(exclude_unset=True).items():
        setattr(staff, key, value)

    session.add(staff)
    session.commit()
    session.refresh(staff)
    return staff

