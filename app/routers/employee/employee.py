# app/routers/employee.py
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.api.v1.employee.employee.employee_controller import EmployeeController
from app.schemas.employee import EmployeeSkillsList, EmployeeProfile, EmployeeUpdateRequest, TaskSummaryResponse
from app.schemas.employee_skill import EmployeeSkillCreate
from app.services.employee_task_service import EmployeeTaskService
from app.core.security import get_current_employee
from app.schemas.subtask_update import SubtaskUpdateRequest
from app.models.employee import Employee
from pydantic import BaseModel
#router = APIRouter(tags=["Employee"])
from fastapi import APIRouter

class SubtaskStatusResponse(BaseModel):
    id: int
    status: str
router = APIRouter(
    prefix="/employee",
    tags=["Employee"]
)
@router.get(
    "/skills",
    response_model=EmployeeSkillsList,
    status_code=status.HTTP_200_OK
)

def get_my_skills_endpoint(
    db: Session = Depends(get_session),
    current_employee: Employee = Depends(get_current_employee)
):
    return {"skills": EmployeeController.get_my_skills(db, current_employee)}
####################################################################

@router.post(
    "/skills",
    status_code=status.HTTP_201_CREATED
)
def add_employee_skill_endpoint(
    skill_data: EmployeeSkillCreate,
    db: Session = Depends(get_session),
    current_employee: Employee = Depends(get_current_employee)
):
    
    EmployeeController.add_employee_skill(current_employee.id, skill_data, db)
    return {"message": "Skill added successfully."}
########################################################################################
@router.get(
    "/profile",
    response_model=EmployeeProfile,
    status_code=status.HTTP_200_OK
)
def get_employee_profile_endpoint(
    db: Session = Depends(get_session),
    current_employee: Employee = Depends(get_current_employee)
):
    return EmployeeController.get_my_profile(db, current_employee)
##############################################################################################
@router.put(
    "/profile",
    response_model=EmployeeProfile,
    status_code=status.HTTP_200_OK
)
def update_employee_profile_endpoint(
    update_data: EmployeeUpdateRequest,
    db: Session = Depends(get_session),
    current_employee: Employee = Depends(get_current_employee)
):
    updated_employee = EmployeeController.update_my_profile(db, current_employee, update_data)
    return updated_employee
########################################################################################################

@router.get("/tasks", status_code=status.HTTP_200_OK)
def get_employee_tasks_endpoint(
    db: Session = Depends(get_session),
    current_employee: Employee = Depends(get_current_employee)
):
    tasks = EmployeeTaskService.get_employee_tasks(db, current_employee.id)
    return tasks
#############################################################################
@router.put("/subtasks/{subtask_id}/status", status_code=status.HTTP_200_OK)
def update_subtask_status_endpoint(
    subtask_id: int,
    request: SubtaskUpdateRequest,
    db: Session = Depends(get_session),
    current_employee: Employee = Depends(get_current_employee)
):
    subtask = EmployeeTaskService.update_subtask_status(
        db, current_employee.id, subtask_id, request.status
    )
    return {"id": subtask.id, "status": subtask.status.value}