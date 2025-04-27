from sqlmodel import SQLModel, Field
from typing import Optional

class LabTest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    requested_by: int = Field(foreign_key="staff.id")
    lab_id: int = Field(foreign_key="department.id")
    result_file_url: Optional[str] = None
    status: str
