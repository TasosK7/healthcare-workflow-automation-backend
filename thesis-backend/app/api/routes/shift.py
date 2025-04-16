from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List

from app.db.session import get_session
from app.core.auth import get_current_admin, get_current_admin_or_hr
from app.models.user import User
from app.schemas.shift import ShiftCreate, ShiftRead
from app.crud.shift import create_shift, get_shifts

router = APIRouter()

@router.post("/", response_model=ShiftRead, status_code=201)
def create_shift_route(
    shift_in: ShiftCreate,
    session: Session = Depends(get_session),
    current_admin_or_hr: User = Depends(get_current_admin_or_hr)
):
    return create_shift(shift_in, session)

@router.get("/", response_model=List[ShiftRead])
def list_shifts(
    session: Session = Depends(get_session),
    current_admin_or_hr: User = Depends(get_current_admin_or_hr)
):
    return get_shifts(session)
