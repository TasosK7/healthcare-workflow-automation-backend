from fastapi import HTTPException, status
from sqlmodel import Session, select
from typing import List
from app.models.patient import Patient
from app.models.user import User
from app.schemas.patient import PatientCreate

def create_patient(patient_in: PatientCreate, session: Session) -> Patient:
    user = session.get(User, patient_in.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user.role != "patient":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not have the 'patient' role"
        )

    patient = Patient(**patient_in.model_dump())
    session.add(patient)
    session.commit()
    session.refresh(patient)
    return patient

def get_patients(session: Session) -> List[Patient]:
    return session.exec(select(Patient)).all()
