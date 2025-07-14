from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from app.db.session import get_session
from app.schemas.department import DepartmentCreate, DepartmentRead, DepartmentUpdate
from app.crud.department import create_department, get_departments, update_department
from app.core.auth import get_current_admin
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=DepartmentRead, status_code=201)
def create(
    dept_in: DepartmentCreate,
    session: Session = Depends(get_session),
    current_admin: User = Depends(get_current_admin)
):
    return create_department(dept_in, session)

@router.get("/", response_model=List[DepartmentRead])
def list_departments(session: Session = Depends(get_session)):
    return get_departments(session)

@router.put("/{id}", response_model=DepartmentRead)
def update(
    id: int,
    dept_in: DepartmentUpdate,
    session: Session = Depends(get_session),
    current_admin: User = Depends(get_current_admin)
):
    return update_department(id, dept_in, session)
