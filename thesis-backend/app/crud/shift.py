from fastapi import HTTPException, status
from sqlmodel import Session, select
from typing import List
from app.models.shift import Shift
from app.models.staff import Staff
from app.schemas.shift import ShiftCreate

def create_shift(shift_in: ShiftCreate, session: Session) -> Shift:
    staff = session.get(Staff, shift_in.staff_id)
    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff member not found"
        )

    existing_shift = session.exec(
        select(Shift).where(
            Shift.staff_id == shift_in.staff_id,
            Shift.date == shift_in.date
        )
    ).first()

    if existing_shift:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Staff already has a shift assigned on this date"
        )

    shift = Shift(**shift_in.model_dump())
    session.add(shift)
    session.commit()
    session.refresh(shift)
    return shift

def get_shifts(session: Session) -> List[Shift]:
    return session.exec(select(Shift)).all()
