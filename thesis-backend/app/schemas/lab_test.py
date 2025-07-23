from pydantic import BaseModel, EmailStr
from typing import Optional

class LabTestBase(BaseModel):
    patient_id: int
    staff_id: int
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

class LabTestForAirflow(BaseModel):
    id: int
    patient_id: int
    result_file_url: Optional[str]
    status: str
    diagnosis: Optional[str]
    patient_name: str
    patient_email: EmailStr
    staff_email: EmailStr

    class Config:
        orm_mode = True

class LabTestWithStaffName(BaseModel):
    id: int
    result_file_url: Optional[str]
    diagnosis: Optional[str]
    staff_name: str

    class Config:
        orm_mode = True


