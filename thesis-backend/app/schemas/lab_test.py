from pydantic import BaseModel
from typing import Optional

class LabTestBase(BaseModel):
    patient_id: int
    requested_by: Optional[int] = None
    lab_id: Optional[int] = None
    result_file_url: Optional[str] = None
    status: str

class LabTestCreate(LabTestBase):
    pass

class LabTestRead(LabTestBase):
    id: int

    class Config:
        orm_mode = True
