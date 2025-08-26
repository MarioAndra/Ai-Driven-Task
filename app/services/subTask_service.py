
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.subtask import Subtask
from app.models.employee import Employee
from app.models.Assignment import Assignment
from app.services.email_service import EmailService


class SubTaskService:
    @staticmethod
    def create_assignment(db: Session, assignment_data: dict):

        subtask_id = assignment_data.get("subtask_id")
        employee_id = assignment_data.get("employee_id")

        if not subtask_id or not employee_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Subtask ID and Employee ID are required.")

        subtask = db.get(Subtask, subtask_id)
        if not subtask:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Subtask with id {subtask_id} not found.")

        employee = db.get(Employee, employee_id)
        if not employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Employee with id {employee_id} not found.")

        existing_assignment = db.exec(select(Assignment).where(Assignment.sub_task_id == subtask_id)).scalars().first()
        if existing_assignment and existing_assignment.employee_id is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Subtask {subtask_id} is already assigned.")

        if existing_assignment:
            assignment = existing_assignment
            assignment.employee_id = employee_id
        else:
            assignment = Assignment(sub_task_id=subtask_id, employee_id=employee_id)

        db.add(assignment)
        db.commit()
        db.refresh(assignment)


        print(f"  -> Sending assignment email to {employee.email}...")
        EmailService.send_email(
            subject="New Task Assigned",
            recipients=[employee.email],
            template_name="assignment_notification.html",
            template_body={
                "employee_name": employee.name,
                "subtask_description": subtask.description
            }
        )

        return {"message": "Subtask assigned successfully.", "assignment_id": assignment.id, "subtask_id": subtask.id,
                "employee_id": employee.id}

    @staticmethod
    def update_assignment(db: Session, assignment_id: int, update_data: dict):

        new_employee_id = update_data.get("employee_id")
        if not new_employee_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New Employee ID is required.")

        assignment = db.get(Assignment, assignment_id)
        if not assignment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Assignment with id {assignment_id} not found.")


        subtask = db.get(Subtask, assignment.sub_task_id)
        if not subtask:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated subtask not found.")

        new_employee = db.get(Employee, new_employee_id)
        if not new_employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Employee with id {new_employee_id} not found.")

        assignment.employee_id = new_employee_id
        db.add(assignment)
        db.commit()
        db.refresh(assignment)


        print(f"  -> Sending re-assignment email to {new_employee.email}...")
        EmailService.send_email(
            subject="A Task Has Been Re-assigned to You",
            recipients=[new_employee.email],
            template_name="assignment_notification.html",
            template_body={
                "employee_name": new_employee.name,
                "subtask_description": subtask.description
            }
        )

        return {"message": "Assignment updated successfully.", "assignment_id": assignment.id,
                "new_employee_id": new_employee.id}

    @staticmethod
    def delete_assignment(db: Session, assignment_id: int):

        assignment = db.get(Assignment, assignment_id)
        if not assignment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Assignment with id {assignment_id} not found.")

        db.delete(assignment)
        db.commit()
        return {"message": "Assignment deleted successfully."}
