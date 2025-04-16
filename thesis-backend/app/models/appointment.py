from sqlmodel import SQLModel, Field
from datetime import date
from typing import Optional

class Appointment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    staff_id: int = Field(foreign_key="staff.id")
    date: date
    status: str
