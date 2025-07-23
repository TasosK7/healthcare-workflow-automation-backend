from pydantic import BaseModel, EmailStr
from datetime import date

class AppointmentBase(BaseModel):
    patient_id: int
    staff_id: int
    date: date
    status: str

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentRead(AppointmentBase):
    id: int

    class Config:
        orm_mode = True

class AppointmentWithStaffName(BaseModel):
    id: int
    staff_id: int
    date: date
    status: str
    staff_name: str

    class Config:
        orm_mode = True

class AppointmentWithPatientName(BaseModel):
    id: int
    date: date
    status: str
    patient_id: int
    patient_name: str

    class Config:
        orm_mode = True


class AppointmentForAirflow(AppointmentWithStaffName):
    patient_email: EmailStr
    staff_email: EmailStr
    email_sent: bool
    reminder_sent: bool

    class Config:
        orm_mode = True



