from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlmodel import Session, select
from app.services.minio_client import minio_client, BUCKET_NAME
import os
import uuid
from typing import List

from app.db.session import get_session
from app.core.auth import get_current_admin,get_current_admin_or_lab_tech, get_current_user
from app.models.user import User
from app.models.lab_test import LabTest
from app.models.patient import Patient
from app.schemas.lab_test import LabTestCreate, LabTestRead
from app.crud.lab_test import create_lab_test, get_lab_tests

router = APIRouter()

@router.post("/", response_model=LabTestRead, status_code=201)
def create_lab_test_route(
    lab_in: LabTestCreate,
    session: Session = Depends(get_session),
    current_admin: User = Depends(get_current_admin)
):
    return create_lab_test(lab_in, session)

@router.get("/", response_model=List[LabTestRead])
def list_lab_tests(
    session: Session = Depends(get_session),
    current_admin: User = Depends(get_current_admin_or_lab_tech)
):
    return get_lab_tests(session)


from app.services.minio_client import minio_client, BUCKET_NAME
import uuid

@router.post("/upload", response_model=LabTestRead)
async def upload_lab_test(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if current_user.role != "patient":
        raise HTTPException(status_code=403, detail="Patients only")

    patient = session.exec(select(Patient).where(Patient.user_id == current_user.id)).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Generate unique object name
    object_name = f"{uuid.uuid4()}_{file.filename}"

    # Upload to MinIO
    minio_client.put_object(
        bucket_name=BUCKET_NAME,
        object_name=object_name,
        data=file.file,
        length=-1,
        part_size=10 * 1024 * 1024,
        content_type=file.content_type
    )

    file_url = f"http://localhost:9001/{BUCKET_NAME}/{object_name}"

    lab_test = LabTest(
        patient_id=patient.id,
        result_file_url=file_url,
        status="submitted"
    )
    session.add(lab_test)
    session.commit()
    session.refresh(lab_test)
    return lab_test
