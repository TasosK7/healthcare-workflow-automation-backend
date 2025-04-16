from pydantic import BaseModel
from typing import Optional

class StaffBase(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    department_id: Optional[int] = None
    role: str

class StaffCreate(StaffBase):
    pass

class StaffRead(StaffBase):
    id: int

    class Config:
        orm_mode = True
