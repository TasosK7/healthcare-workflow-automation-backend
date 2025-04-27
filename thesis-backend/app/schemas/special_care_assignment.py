from pydantic import BaseModel
from datetime import date
from typing import Optional

class SpecialCareAssignmentBase(BaseModel):
    patient_id: int
    staff_id: Optional[int] = None
    unit_name: str
    admission_date: date
    status: str

class SpecialCareAssignmentCreate(SpecialCareAssignmentBase):
    pass

class SpecialCareAssignmentRead(SpecialCareAssignmentBase):
    id: int

    class Config:
        orm_mode = True
