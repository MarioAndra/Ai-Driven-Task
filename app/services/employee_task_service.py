
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.task import Task
from app.models.subtask import Subtask, SubtaskStatus
from app.models.Assignment import Assignment
from app.models.employee import Employee
from app.models.Admin import Admin
from app.services.email_service import EmailService
from typing import Optional


class EmployeeTaskService:
    @staticmethod
    def get_employee_tasks(db: Session, employee_id: int, subtask_status: Optional[str] = None) -> list[dict]:

        stmt = (
            select(Assignment)
            .where(Assignment.employee_id == employee_id)
            .options(selectinload(Assignment.subtask).selectinload(Subtask.parent_task))
        )
        assignments = db.exec(stmt).scalars().all()

        task_map = {}
        for assign in assignments:
            subtask = assign.subtask
            if not subtask: continue
            if subtask_status and subtask.status.value != subtask_status: continue
            parent_task = subtask.parent_task
            if not parent_task: continue

            if parent_task.id not in task_map:
                task_map[parent_task.id] = {
                    "parent_task": {"id": parent_task.id, "description": parent_task.description},
                    "assigned_subtasks": []
                }

            task_map[parent_task.id]["assigned_subtasks"].append({
                "id": subtask.id, "description": subtask.description, "status": subtask.status.value
            })
        return list(task_map.values())

    @staticmethod
    def update_subtask_status(db: Session, employee_id: int, subtask_id: int, update_data: dict) -> dict:

        new_status_str = update_data.get("status")
        if not new_status_str:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Status is required.")

        try:
            new_status = SubtaskStatus(new_status_str)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid status: {new_status_str}")

        assignment = db.exec(select(Assignment).where(Assignment.employee_id == employee_id,
                                                      Assignment.sub_task_id == subtask_id)).first()
        if not assignment:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not assigned to this subtask.")

        subtask = db.get(Subtask, subtask_id)
        if not subtask:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subtask not found.")

        subtask.status = new_status
        db.add(subtask)
        db.commit()
        db.refresh(subtask)

        if new_status == SubtaskStatus.completed:

            project_manager = db.exec(select(Admin).where(Admin.role == 'admin')).scalars().first()
            employee = db.get(Employee, employee_id)

            if project_manager and employee:
                print(f"  -> Sending completion email to {project_manager.email}...")
                EmailService.send_email(
                    subject=f"Task Completed by {employee.name}",
                    recipients=[project_manager.email],
                    template_name="task_completed_notification.html",
                    template_body={
                        "employee_name": employee.name,
                        "subtask_description": subtask.description,
                        "project_manager":project_manager.name
                    }
                )

        return {"id": subtask.id, "description": subtask.description, "status": subtask.status.value}
