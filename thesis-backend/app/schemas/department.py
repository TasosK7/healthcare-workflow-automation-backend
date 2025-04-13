from pydantic import BaseModel

class DepartmentBase(BaseModel):
    name: str
    unit_type: str

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentRead(DepartmentBase):
    id: int

    class Config:
        orm_mode = True
