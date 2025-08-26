# app/routers/employee/task.py
from fastapi import APIRouter, Depends, status, Request, Query
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.api.v1.employee.employee_task_controller import EmployeeTaskController
from app.core.security import get_current_employee
from app.models.employee import Employee
from typing import Optional

router = APIRouter(
    prefix="/tasks",
    tags=["Employee Tasks "]
)

@router.get("/", summary="Get my assigned tasks with subtasks")
def get_my_tasks_endpoint(
    status: Optional[str] = Query(None, description="Filter subtasks by status (e.g., pending, in_progress, completed)"),
    db: Session = Depends(get_session),
    current_employee: Employee = Depends(get_current_employee)
):
    return EmployeeTaskController.get_my_tasks(db, current_employee, status)

@router.put("/subtasks/{subtask_id}/status", summary="Update status of my subtask")
async def update_my_subtask_status_endpoint(
    subtask_id: int,
    request: Request,
    db: Session = Depends(get_session),
    current_employee: Employee = Depends(get_current_employee)
):
    update_data = await request.json()
    return EmployeeTaskController.update_my_subtask_status(db, current_employee, subtask_id, update_data)
