from pydantic import EmailStr
from sqlmodel import SQLModel, Field
from typing import Optional

class Patient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    first_name: str
    last_name: str
    email: EmailStr
