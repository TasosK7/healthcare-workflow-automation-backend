from sqlmodel import Session, select
from fastapi import HTTPException
from app.models.department import Department
from app.schemas.department import DepartmentCreate
from app.schemas.department import DepartmentUpdate
from typing import List

def create_department(dept_in: DepartmentCreate, session: Session) -> Department:
    dept = Department(**dept_in.model_dump())
    session.add(dept)
    session.commit()
    session.refresh(dept)
    return dept

def get_departments(session: Session) -> List[Department]:
    statement = select(Department)
    results = session.exec(statement).all()
    return results

def update_department(id: int, dept_in: DepartmentUpdate, session: Session) -> Department:
    dept = session.get(Department, id)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")

    for key, value in dept_in.model_dump(exclude_unset=True).items():
        setattr(dept, key, value)

    session.add(dept)
    session.commit()
    session.refresh(dept)
    return dept
