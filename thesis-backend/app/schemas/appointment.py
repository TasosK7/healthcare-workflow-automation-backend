from pydantic import BaseModel
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
