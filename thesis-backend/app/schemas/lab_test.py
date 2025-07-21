from pydantic import BaseModel
from typing import Optional

class LabTestBase(BaseModel):
    patient_id: int
    requested_by: Optional[int] = None
    lab_id: Optional[int] = None
    result_file_url: Optional[str] = None
    status: str
    diagnosis: Optional[str] = None

class LabTestCreate(LabTestBase):
    pass

class LabTestRead(LabTestBase):
    id: int

    class Config:
        orm_mode = True

class LabTestUpdate(BaseModel):
    diagnosis: Optional[str] = None

class LabTestWithPatientName(BaseModel):
    id: int
    patient_id: int
    result_file_url: Optional[str]
    status: str
    diagnosis: Optional[str] = None
    patient_name: str

    class Config:
        orm_mode = True

class LabTestWithStaffName(BaseModel):
    id: int
    result_file_url: Optional[str]
    diagnosis: Optional[str]
    staff_name: str

    class Config:
        orm_mode = True


