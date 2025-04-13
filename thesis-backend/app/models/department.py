from sqlmodel import SQLModel, Field
from typing import Optional

class Department(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    unit_type: str
