from sqlmodel import Session, select
from app.models.department import Department
from app.schemas.department import DepartmentCreate
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
