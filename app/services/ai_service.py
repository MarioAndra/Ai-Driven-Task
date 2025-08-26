from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from typing import List
import json
from app.models.employee import Employee
from app.models.EmployeeSkillLink import EmployeeSkillLink
from app.models.subtask import Subtask
from app.models.Assignment import Assignment
from app.ai import task_assessor
from pathlib import Path
from app.services.email_service import EmailService

class AIService:
    @staticmethod
    def format_employees_for_ai(db: Session) -> List[dict]:
        statement = select(Employee).options(
            selectinload(Employee.skills),
            selectinload(Employee.assignments).selectinload(Assignment.subtask)
        )
        employees_from_db = db.exec(statement).unique().all()

        formatted_employees = []
        for emp in employees_from_db:
            if emp.status != 'available':
                continue

            skills_list = []
            for skill in emp.skills:
                link_statement = select(EmployeeSkillLink).where(
                    EmployeeSkillLink.employee_id == emp.id,
                    EmployeeSkillLink.skill_id == skill.id
                )
                link = db.exec(link_statement).first()
                if link:
                    skills_list.append({"name": skill.name, "rating": link.rating})

            active_assignments = [
                a for a in emp.assignments
                if a.subtask and a.subtask.status != 'completed'
            ]
            current_assigned_tasks = len(active_assignments)

            formatted_employees.append({
                "name": emp.name,
                "skills": skills_list,
                "status": emp.status.value,
                "assigned_tasks": [None] * current_assigned_tasks,
                "task_capacity": emp.task_capacity,
                "available_hours": emp.available_hours
            })
        return formatted_employees

    @staticmethod
    def get_assignments_for_tasks(db: Session, subtasks: List[Subtask]) -> List[dict]:
        employees_data = AIService.format_employees_for_ai(db)
        current_weights = task_assessor.load_model_weights()
        subtask_descriptions = [st.description for st in subtasks]
        print("-> [AIService] Trying to assign tasks with AI model...",flush=True)


        assignments_result, _ = task_assessor.assign_tasks_with_learning(
            subtasks=subtask_descriptions,
            employees=employees_data,
            model_weights=current_weights
        )
        print("-> [AIService] AI assignment finished.", flush=True)

        new_assignments = []
        for i, result in enumerate(assignments_result):
            if result.get("employee_name"):
                emp_statement = select(Employee).where(Employee.name == result["employee_name"])
                employee = db.exec(emp_statement).first()

                if employee:
                    features = result.get("features", {})
                    new_assignment = Assignment(
                        sub_task_id=subtasks[i].id,
                        employee_id=employee.id,
                        match_score=features.get("match_score"),
                        avg_skill_level=features.get("avg_skill_level"),
                        availability=features.get("availability"),
                        current_load=features.get("current_load")
                    )
                    db.add(new_assignment)
                    new_assignments.append(new_assignment)


                    print(f"  -> Attempting to send email to {employee.name}...", flush=True)
                    EmailService.send_email(
                        subject="New Task Assigned to You",
                        recipients=[employee.email],
                        template_name="assignment_notification.html",
                        template_body={
                            "employee_name": employee.name,
                            "subtask_description": subtasks[i].description,
                        }
                    )

        db.commit()

        assignments_with_details = []
        for assignment in new_assignments:
            db.refresh(assignment)
            subtask_description = assignment.subtask.description if assignment.subtask else "N/A"
            employee_name = assignment.employee.name if assignment.employee else "N/A"
            assignments_with_details.append({
                "id": assignment.id,
                "sub_task_id": assignment.sub_task_id,
                "sub_task_description": subtask_description,
                "employee_id": assignment.employee_id,
                "employee_name": employee_name,
                "match_score": assignment.match_score,
                "avg_skill_level": assignment.avg_skill_level,
                "availability": assignment.availability,
                "current_load": assignment.current_load,
                "feedback": assignment.feedback,
                "created_at": assignment.created_at,
                "updated_at": assignment.updated_at
            })

        return assignments_with_details
