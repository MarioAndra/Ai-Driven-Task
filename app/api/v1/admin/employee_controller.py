from typing import Optional
from fastapi import HTTPException
from sqlmodel import Session

from app.services import employee_service
from app.models.employee import EmployeeStatus

from app.schemas.employee import EmployeeUpdateRequest


def index_employees_controller(session: Session, status: Optional[EmployeeStatus] = None):
    employees = employee_service.get_all_employees(session, status=status)
    return employees


def show_employee_controller(session: Session, employee_id: int):
    employee = employee_service.get_employee_by_id(session, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    tasks_map = {}
    for assignment in employee.assignments:
        subtask = assignment.subtask
        if subtask and subtask.parent_task:
            parent_task = subtask.parent_task
            if parent_task.id not in tasks_map:
                tasks_map[parent_task.id] = {
                    "parent_task": parent_task,
                    "assigned_subtasks": []
                }
            tasks_map[parent_task.id]["assigned_subtasks"].append(subtask)

    return {
        "employee": employee,
        "tasks_summary": list(tasks_map.values())
    }


def update_employee_controller(session: Session, employee_id: int, request: EmployeeUpdateRequest):
    employee = employee_service.get_employee_by_id(session, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    if not request.model_dump(exclude_unset=True):
        raise HTTPException(status_code=400, detail="No update data provided")

    updated_employee = employee_service.update_employee_details(session, employee, request)
    return updated_employee
