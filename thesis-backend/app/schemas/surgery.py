from pydantic import BaseModel

class SurgeryBase(BaseModel):
    appointment_id: int
    referred_by: int
    surgeon_id: int
    status: str
    
class SurgeryCreate(SurgeryBase):
    pass

class SurgeryRead(SurgeryBase):
    id: int

    class Config:
        orm_mode = True
