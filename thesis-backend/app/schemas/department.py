from pydantic import BaseModel
from typing import Optional

class DepartmentBase(BaseModel):
    name: str
    unit_type: str

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    unit_type: Optional[str] = None

class DepartmentRead(DepartmentBase):
    id: int

    class Config:
        orm_mode = True
