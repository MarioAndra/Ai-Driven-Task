from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.employee import Employee
from app.models.skill import Skill
from app.models.EmployeeSkillLink import EmployeeSkillLink
from sqlalchemy import select


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
            "available_hours": employee.available_hours
        }

    @staticmethod
    def update_employee_profile(
        db: Session, employee_id: int, update_data: dict
    ) -> dict:
        employee = db.get(Employee, employee_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found."
            )

        for key, value in update_data.items():
            setattr(employee, key, value)

        db.add(employee)
        db.commit()
        db.refresh(employee)

        return EmployeeProfileService.get_employee_profile(db, employee.id)
