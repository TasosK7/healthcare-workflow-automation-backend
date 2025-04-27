from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List

from app.db.session import get_session
from app.core.auth import get_current_admin,get_current_admin_or_lab_tech
from app.models.user import User
from app.schemas.lab_test import LabTestCreate, LabTestRead
from app.crud.lab_test import create_lab_test, get_lab_tests

router = APIRouter()

@router.post("/", response_model=LabTestRead, status_code=201)
def create_lab_test_route(
    lab_in: LabTestCreate,
    session: Session = Depends(get_session),
    current_admin: User = Depends(get_current_admin)
):
    return create_lab_test(lab_in, session)

@router.get("/", response_model=List[LabTestRead])
def list_lab_tests(
    session: Session = Depends(get_session),
    current_admin: User = Depends(get_current_admin_or_lab_tech)
):
    return get_lab_tests(session)   
