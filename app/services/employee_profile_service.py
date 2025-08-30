from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.employee import Employee
from app.models.skill import Skill
from app.models.EmployeeSkillLink import EmployeeSkillLink
from sqlalchemy import select
from app.core.security import hash_password


class EmployeeProfileService:
    @staticmethod
    def get_employee_profile(db: Session, employee_id: int) -> dict:
        employee = db.get(Employee, employee_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found."
            )

        result = db.execute(
            select(
                EmployeeSkillLink.skill_id,
                Skill.name,
                EmployeeSkillLink.rating
            )
            .join(Skill, Skill.id == EmployeeSkillLink.skill_id)
            .where(EmployeeSkillLink.employee_id == employee_id)
        ).all()

        skills_list = [
            {"skill_id": skill_id, "name": name, "rating": rating}
            for skill_id, name, rating in result
        ]

        return {
            "id": employee.id,
            "name": employee.name,
            "email": employee.email,
            "phone_number": employee.phone_number,
            "address": employee.address,
            "birth_date": employee.birth_date,
            "skills": skills_list,
            "task_capacity": employee.task_capacity,
            "available_hours": employee.available_hours,
            "status": employee.status
        }

    @staticmethod
    def update_employee_profile(
        db: Session,
        employee_id: int,
        update_data: dict
    ) -> dict:
        employee = db.get(Employee, employee_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found."
            )

        # Handle email updates
        if "email" in update_data and update_data["email"] is not None:
            new_email = update_data["email"]
            if new_email != employee.email:
                existing_employee = db.query(Employee).filter(Employee.email == new_email).first()
                if existing_employee:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Email already registered by another user."
                    )
                employee.email = new_email
            del update_data["email"]

        # Handle password updates
        if "password" in update_data and update_data["password"] is not None:
            new_password = update_data["password"]
            employee.password = hash_password(new_password)
            del update_data["password"]

        # Update other fields dynamically
        for key, value in update_data.items():
            setattr(employee, key, value)

        db.add(employee)
        db.commit()
        db.refresh(employee)

        return EmployeeProfileService.get_employee_profile(db, employee.id)
