from pydantic import BaseModel

class PatientBase(BaseModel):
    user_id: int
    first_name: str
    last_name: str

class PatientCreate(PatientBase):
    pass

class PatientRead(PatientBase):
    id: int

    class Config:
        orm_mode = True
