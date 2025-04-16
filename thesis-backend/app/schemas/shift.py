from pydantic import BaseModel
from datetime import date

class ShiftBase(BaseModel):
    staff_id: int
    date: date
    shift_type: str
    
class ShiftCreate(ShiftBase):
    pass

class ShiftRead(ShiftBase):
    id: int

    class Config:
        orm_mode = True
