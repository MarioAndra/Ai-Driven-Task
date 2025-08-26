# app/routers/employee/skill.py
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.api.v1.employee.employee_skill_controller import EmployeeSkillController
from app.core.security import get_current_employee
from app.models.employee import Employee

router = APIRouter(
    prefix="/skills",
    tags=["Employee Skills "]
)

@router.get("/", summary="Get all my skills")
def get_my_skills_endpoint(
    db: Session = Depends(get_session),
    current_employee: Employee = Depends(get_current_employee)
):
    return EmployeeSkillController.get_my_skills(db, current_employee)

@router.post("/", status_code=status.HTTP_201_CREATED, summary="Add a new skill")
async def add_my_skill_endpoint(
    request: Request,
    db: Session = Depends(get_session),
    current_employee: Employee = Depends(get_current_employee)
):
    skill_data = await request.json()
    return EmployeeSkillController.add_my_skill(db, current_employee, skill_data)

@router.put("/{skill_id}", summary="Update a skill rating")
async def update_my_skill_endpoint(
    skill_id: int,
    request: Request,
    db: Session = Depends(get_session),
    current_employee: Employee = Depends(get_current_employee)
):
    update_data = await request.json()
    return EmployeeSkillController.update_my_skill(db, current_employee, skill_id, update_data)

@router.delete("/{skill_id}", status_code=status.HTTP_200_OK, summary="Delete a skill")
def delete_my_skill_endpoint(
    skill_id: int,
    db: Session = Depends(get_session),
    current_employee: Employee = Depends(get_current_employee)
):
    return EmployeeSkillController.delete_my_skill(db, current_employee, skill_id)
