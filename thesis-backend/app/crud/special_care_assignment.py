from fastapi import HTTPException, status
from sqlmodel import Session, select
from typing import List

from app.models.special_care_assignment import SpecialCareAssignment
from app.models.patient import Patient
from app.models.staff import Staff
from app.schemas.special_care_assignment import SpecialCareAssignmentCreate

def create_special_care_assignment(data: SpecialCareAssignmentCreate, session: Session) -> SpecialCareAssignment:
    if not session.get(Patient, data.patient_id):
        raise HTTPException(status_code=404, detail="Patient not found")

    if data.staff_id is not None and not session.get(Staff, data.staff_id):
        raise HTTPException(status_code=404, detail="Assigned staff not found")

    assignment = SpecialCareAssignment(**data.model_dump())
    session.add(assignment)
    session.commit()
    session.refresh(assignment)
    return assignment

def get_special_care_assignments(session: Session) -> List[SpecialCareAssignment]:
    return session.exec(select(SpecialCareAssignment)).all()
