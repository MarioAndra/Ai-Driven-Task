from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.api.v1.admin.employee_skill_controller import EmployeeSkillController
from app.schemas.employee_skill import EmployeeSkillCreate, EmployeeSkillUpdate, EmployeeSkillRead
from app.core.database import get_session

router = APIRouter()


@router.get("/{employee_id}", response_model=List[EmployeeSkillRead])
def get_employee_skills(employee_id: int, db: Session = Depends(get_session)):
    return EmployeeSkillController.get_employee_skills(employee_id, db)


@router.post("/{employee_id}")
def add_employee_skill(employee_id: int, skill_data: EmployeeSkillCreate, db: Session = Depends(get_session)):
    return EmployeeSkillController.add_employee_skill(employee_id, skill_data, db)


@router.put("/{employee_id}/{skill_id}")
def update_employee_skill(employee_id: int, skill_id: int, skill_data: EmployeeSkillUpdate, db: Session = Depends(get_session)):
    return EmployeeSkillController.update_employee_skill(employee_id, skill_id, skill_data, db)


@router.delete("/{employee_id}/{skill_id}")
def delete_employee_skill(employee_id: int, skill_id: int, db: Session = Depends(get_session)):
    return EmployeeSkillController.delete_employee_skill(employee_id, skill_id, db)
