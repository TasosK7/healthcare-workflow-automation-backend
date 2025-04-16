from fastapi import HTTPException, status
from sqlmodel import Session, select
from typing import List
from app.models.appointment import Appointment
from app.models.patient import Patient
from app.models.staff import Staff
from app.schemas.appointment import AppointmentCreate

def create_appointment(appt_in: AppointmentCreate, session: Session) -> Appointment:
    patient = session.get(Patient, appt_in.patient_id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    staff = session.get(Staff, appt_in.staff_id)
    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff member not found"
        )

    appt = Appointment(**appt_in.model_dump())
    session.add(appt)
    session.commit()
    session.refresh(appt)
    return appt

def get_appointments(session: Session) -> List[Appointment]:
    return session.exec(select(Appointment)).all()
