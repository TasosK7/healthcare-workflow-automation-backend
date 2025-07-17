from fastapi import APIRouter, Depends , HTTPException
from sqlmodel import Session, select
from typing import List

from app.db.session import get_session
from app.core.auth import get_current_admin, get_current_user
from app.services.airflow import trigger_appointment_dag
from app.models.user import User
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.models.staff import Staff
from app.schemas.appointment import AppointmentCreate, AppointmentRead, AppointmentWithStaffName, AppointmentForAirflow
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

@router.get("/me", response_model=List[AppointmentWithStaffName])
def get_my_appointments(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "patient":
        raise HTTPException(status_code=403, detail="Patients only")

    patient = session.exec(
        select(Patient).where(Patient.user_id == current_user.id)
    ).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient record not found")

    appointments = session.exec(
        select(Appointment).where(Appointment.patient_id == patient.id)
    ).all()

    enriched_appointments = []
    for appt in appointments:
        staff = session.get(Staff, appt.staff_id)
        enriched_appointments.append(AppointmentWithStaffName(
            id=appt.id,
            staff_id=appt.staff_id,
            date=appt.date,
            status=appt.status,
            staff_name=f"{staff.first_name} {staff.last_name}"
        ))

    return enriched_appointments

@router.get("/{appointment_id}", response_model=AppointmentForAirflow)
def get_appointment_details(
    appointment_id: int,
    session: Session = Depends(get_session),
):
    appt = session.get(Appointment, appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")

    staff = session.get(Staff, appt.staff_id)

    return AppointmentForAirflow(
        id=appt.id,
        staff_id=appt.staff_id,
        date=appt.date,
        status=appt.status,
        staff_name=f"{staff.first_name} {staff.last_name}",
        email_sent=appt.email_sent,
        reminder_sent=appt.reminder_sent
    )
@router.post("/book", response_model=AppointmentRead, status_code=201)
def book_appointment(
    appt_in: AppointmentCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "patient":
        raise HTTPException(status_code=403, detail="Patients only")

    patient = session.exec(select(Patient).where(Patient.user_id == current_user.id)).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient record not found")

    new_appt = Appointment(
        patient_id=patient.id,
        staff_id=appt_in.staff_id,
        date=appt_in.date,
        status="pending"
    )

    session.add(new_appt)
    session.commit()
    session.refresh(new_appt)

    try:
        trigger_appointment_dag(new_appt.id)
    except Exception as e:
        print(f"Warning: Failed to trigger Airflow DAG: {e}")

    return new_appt

@router.post("/{appointment_id}/mark-email")
def mark_email_sent(appointment_id: int, session: Session = Depends(get_session)):
    appt = session.get(Appointment, appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    appt.email_sent = True
    session.add(appt)
    session.commit()
    return {"status": "ok"}

@router.post("/{appointment_id}/mark-reminder")
def mark_reminder_sent(appointment_id: int, session: Session = Depends(get_session)):
    appt = session.get(Appointment, appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    appt.reminder_sent = True
    session.add(appt)
    session.commit()
    return {"status": "ok"}


