from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List

from app.db.session import get_session
from app.core.auth import get_current_admin
from app.models.user import User
from app.schemas.special_care_assignment import SpecialCareAssignmentCreate, SpecialCareAssignmentRead
from app.crud.special_care_assignment import create_special_care_assignment, get_special_care_assignments

router = APIRouter()

@router.post("/", response_model=SpecialCareAssignmentRead, status_code=201)
def create_special_care(
    assignment_in: SpecialCareAssignmentCreate,
    session: Session = Depends(get_session),
    current_admin: User = Depends(get_current_admin)
):
    return create_special_care_assignment(assignment_in, session)

@router.get("/", response_model=List[SpecialCareAssignmentRead])
def list_special_care(
    session: Session = Depends(get_session),
    current_admin: User = Depends(get_current_admin)
):
    return get_special_care_assignments(session)
