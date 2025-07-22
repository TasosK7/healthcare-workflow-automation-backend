from pydantic import BaseModel, EmailStr
from typing import Optional

class PatientBase(BaseModel):
    user_id: int
    first_name: str
    last_name: str

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class PatientRead(PatientBase):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True
