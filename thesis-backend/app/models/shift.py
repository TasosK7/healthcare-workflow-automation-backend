from sqlmodel import SQLModel, Field
from datetime import date
from typing import Optional

class Shift(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    staff_id: int = Field(foreign_key="staff.id")
    date: date
    shift_type: str