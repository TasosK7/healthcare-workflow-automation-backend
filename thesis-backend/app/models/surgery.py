from sqlmodel import SQLModel, Field
from typing import Optional

class Surgery(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    appointment_id: int = Field(foreign_key="appointment.id")
    referred_by: int = Field(foreign_key="staff.id")
    surgeon_id: int = Field(foreign_key="staff.id")
    status: str
