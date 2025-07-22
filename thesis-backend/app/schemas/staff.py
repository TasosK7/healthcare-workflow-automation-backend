from pydantic import BaseModel, EmailStr
from typing import Optional

class StaffBase(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    department_id: Optional[int] = None
    role: str

class StaffCreate(StaffBase):
    pass

class StaffUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    department_id: Optional[int] = None
    role: Optional[str] = None

class StaffRead(StaffBase):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True
