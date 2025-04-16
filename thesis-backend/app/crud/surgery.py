from fastapi import HTTPException, status
from sqlmodel import Session, select
from typing import List
from app.models.surgery import Surgery
from app.models.staff import Staff
from app.models.appointment import Appointment
from app.schemas.surgery import SurgeryCreate

def create_surgery(surgery_in: SurgeryCreate, session: Session) -> Surgery:
    appointment = session.get(Appointment, surgery_in.appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    referring = session.get(Staff, surgery_in.referred_by)
    if not referring:
        raise HTTPException(status_code=404, detail="Referring staff not found")

    surgeon = session.get(Staff, surgery_in.surgeon_id)
    if not surgeon:
        raise HTTPException(status_code=404, detail="Surgeon not found")

    surgery = Surgery(**surgery_in.model_dump())
    session.add(surgery)
    session.commit()
    session.refresh(surgery)
    return surgery

def get_surgeries(session: Session) -> List[Surgery]:
    return session.exec(select(Surgery)).all()
