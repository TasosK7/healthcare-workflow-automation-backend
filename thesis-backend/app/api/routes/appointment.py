from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List

from app.db.session import get_session
from app.core.auth import get_current_admin
from app.models.user import User
from app.schemas.appointment import AppointmentCreate, AppointmentRead
from app.crud.appointment import create_appointment, get_appointments

router = APIRouter()

@router.post("/", response_model=AppointmentRead, status_code=201)
def create_appointment_route(
    appt_in: AppointmentCreate,
    session: Session = Depends(get_session),
    current_admin: User = Depends(get_current_admin)
):
    return create_appointment(appt_in, session)

@router.get("/", response_model=List[AppointmentRead])
def list_appointments(
    session: Session = Depends(get_session),
    current_admin: User = Depends(get_current_admin)
):
    return get_appointments(session)
