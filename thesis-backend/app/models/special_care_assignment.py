from sqlmodel import SQLModel, Field
from datetime import date
from typing import Optional

class SpecialCareAssignment(SQLModel, table=True):
    __tablename__ = "special_care_assignment"

    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    staff_id: Optional[int] = Field(default=None, foreign_key="staff.id")
    unit_name: str
    admission_date: date
    status: str
