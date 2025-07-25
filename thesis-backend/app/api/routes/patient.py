from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from app.db.session import get_session
from app.core.auth import get_current_admin, get_current_patient, get_current_airflow
from app.models.user import User
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientRead, PatientUpdate
from app.crud.patient import create_patient, get_patients, update_patient

router = APIRouter()

@router.post("/", response_model=PatientRead, status_code=201)
def create(
    patient_in: PatientCreate,
    session: Session = Depends(get_session),
    current_admin: User = Depends(get_current_admin)
):
    return create_patient(patient_in, session)

@router.get("/", response_model=List[PatientRead])
def list_patients(
    session: Session = Depends(get_session),
    current_admin: User = Depends(get_current_admin)
):
    return get_patients(session)

@router.get("/me", response_model=PatientRead)
def read_current_patient(current_patient: Patient = Depends(get_current_patient)):
    return current_patient

@router.get("/{patient_id}", response_model=PatientRead)
def get_patient_by_id(
    patient_id: int,
    session: Session = Depends(get_session),
    current_airflow: User = Depends(get_current_airflow)
):
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.put("/{id}", response_model=PatientRead)
def update(
    id: int,
    patient_in: PatientUpdate,
    session: Session = Depends(get_session),
    current_admin: User = Depends(get_current_admin)
):
    return update_patient(id, patient_in, session)
