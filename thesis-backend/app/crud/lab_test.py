from fastapi import HTTPException, status
from sqlmodel import Session, select
from typing import List

from app.models.lab_test import LabTest
from app.models.patient import Patient
from app.models.staff import Staff
from app.models.department import Department
from app.schemas.lab_test import LabTestCreate

def create_lab_test(lab_in: LabTestCreate, session: Session) -> LabTest:
    if not session.get(Patient, lab_in.patient_id):
        raise HTTPException(status_code=404, detail="Patient not found")

    if not session.get(Staff, lab_in.staff_id):
        raise HTTPException(status_code=404, detail="Assigned staff not found")

    department = session.get(Department, lab_in.lab_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    if department.name.lower() != "laboratory":
        raise HTTPException(
            status_code=400,
            detail="Lab tests can only be assigned to the 'Laboratory' department"
        )

    lab_test = LabTest(**lab_in.model_dump())
    session.add(lab_test)
    session.commit()
    session.refresh(lab_test)
    return lab_test

def get_lab_tests(session: Session) -> List[LabTest]:
    return session.exec(select(LabTest)).all()
