# app/controllers/employee_task_controller.py
from sqlalchemy.orm import Session
from app.services.employee_task_service import EmployeeTaskService
from app.models.employee import Employee
from typing import Optional

class EmployeeTaskController:
    @staticmethod
    def get_my_tasks(db: Session, current_employee: Employee, status: Optional[str] = None):
        return EmployeeTaskService.get_employee_tasks(db, current_employee.id, status)

    @staticmethod
    def update_my_subtask_status(db: Session, current_employee: Employee, subtask_id: int, update_data: dict):
        return EmployeeTaskService.update_subtask_status(db, current_employee.id, subtask_id, update_data)
