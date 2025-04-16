from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List

from app.db.session import get_session
from app.core.auth import get_current_admin
from app.models.user import User
from app.schemas.surgery import SurgeryCreate, SurgeryRead
from app.crud.surgery import create_surgery, get_surgeries

router = APIRouter()

@router.post("/", response_model=SurgeryRead, status_code=201)
def create_surgery_route(
    surgery_in: SurgeryCreate,
    session: Session = Depends(get_session),
    current_admin: User = Depends(get_current_admin)
):
    return create_surgery(surgery_in, session)

@router.get("/", response_model=List[SurgeryRead])
def list_surgeries(
    session: Session = Depends(get_session),
    current_admin: User = Depends(get_current_admin)
):
    return get_surgeries(session)
