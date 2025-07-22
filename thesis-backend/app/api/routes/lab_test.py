from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlmodel import Session, select
from app.services.minio_client import minio_client, BUCKET_NAME
import os
import uuid
from typing import List
from app.services.minio_client import generate_presigned_url
from app.services.airflow import trigger_test_upload_dag, trigger_test_diagnosis_notification_dag


from app.db.session import get_session
from app.core.auth import get_current_admin,get_current_admin_or_lab_tech, get_current_user
from app.models.user import User
from app.models.lab_test import LabTest
from app.models.patient import Patient
from app.models.staff import Staff
from app.schemas.lab_test import LabTestCreate, LabTestRead, LabTestUpdate, LabTestWithPatientName, LabTestWithStaffName
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

@router.get("/staff/me", response_model=List[LabTestWithPatientName])
def get_lab_tests_for_staff(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "staff":
        raise HTTPException(status_code=403, detail="Staff only")

    tests = session.exec(select(LabTest).where(LabTest.status == "submitted")).all()

    enriched = []
    for test in tests:
        patient = session.get(Patient, test.patient_id)
        enriched.append(LabTestWithPatientName(
            id=test.id,
            patient_id=test.patient_id,
            result_file_url=test.result_file_url,
            status=test.status,
            diagnosis=test.diagnosis,
            patient_name=f"{patient.first_name} {patient.last_name}"
        ))

    return enriched

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

    file_url = f"http://localhost:9000/{BUCKET_NAME}/{object_name}"

    lab_test = LabTest(
        patient_id=patient.id,
        result_file_url=file_url,
        status="submitted"
    )
    session.add(lab_test)
    session.commit()
    session.refresh(lab_test)

    try:
        trigger_test_upload_dag(lab_test.id)
    except Exception as e:
        print(f"Warning: Failed to trigger Airflow DAG: {e}")

    return lab_test

@router.patch("/{test_id}/diagnose", response_model=LabTestRead)
def add_diagnosis_to_lab_test(
    test_id: int,
    update: LabTestUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "staff":
        raise HTTPException(status_code=403, detail="Staff only")

    test = session.get(LabTest, test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Lab test not found")

    staff = session.exec(select(Staff).where(Staff.user_id == current_user.id)).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")

    test.diagnosis = update.diagnosis
    test.status = "diagnosed"
    test.requested_by = staff.id

    session.add(test)
    session.commit()
    session.refresh(test)


    try:
        trigger_test_diagnosis_notification_dag(test.id)
    except Exception as e:
        print(f"Warning: Failed to trigger Airflow DAG: {e}")

    return test


@router.get("/download-url/{lab_test_id}")
def get_presigned_download_url(
        lab_test_id: int,
        session: Session = Depends(get_session),
        current_user: User = Depends(get_current_user)
):

    test = session.get(LabTest, lab_test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Lab test not found")

    if current_user.role not in ["staff", "admin", "patient"]:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if current_user.role == "patient":
        patient = session.exec(select(Patient).where(Patient.user_id == current_user.id)).first()
        if not patient or test.patient_id != patient.id:
            raise HTTPException(status_code=403, detail="This test does not belong to you")

    # extract object key from full file_url (after bucket name)
    object_url = test.result_file_url
    object_name = object_url.split("/")[-1]

    try:
        url = generate_presigned_url(object_name)
        return {"url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Presigned URL error: {str(e)}")

@router.get("/diagnosed/me", response_model=List[LabTestWithStaffName])
def get_diagnosed_lab_tests_for_patient(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "patient":
        raise HTTPException(status_code=403, detail="Patients only")

    patient = session.exec(select(Patient).where(Patient.user_id == current_user.id)).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    tests = session.exec(
        select(LabTest).where(
            LabTest.patient_id == patient.id,
            LabTest.status == "diagnosed"
        )
    ).all()

    enriched = []
    for test in tests:
        staff = session.get(Staff, test.requested_by) if test.requested_by else None
        enriched.append(LabTestWithStaffName(
            id=test.id,
            diagnosis=test.diagnosis,
            result_file_url=test.result_file_url,
            staff_name=f"{staff.first_name} {staff.last_name}" if staff else "N/A"
        ))

    return enriched

@router.get("/{lab_test_id}", response_model=LabTestWithPatientName)
def get_lab_test_by_id_with_patient(
    lab_test_id: int,
    session: Session = Depends(get_session)
):
    test = session.get(LabTest, lab_test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Lab test not found")

    patient = session.get(Patient, test.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return LabTestWithPatientName(
        id=test.id,
        patient_id=test.patient_id,
        result_file_url=test.result_file_url,
        status=test.status,
        diagnosis=test.diagnosis,
        patient_name=f"{patient.first_name} {patient.last_name}"
    )

@router.delete("/{lab_test_id}", status_code=204)
def delete_lab_test(
    lab_test_id: int,
    session: Session = Depends(get_session),
    current_admin: User = Depends(get_current_admin)
):
    test = session.get(LabTest, lab_test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Lab test not found")

    session.delete(test)
    session.commit()
    return







