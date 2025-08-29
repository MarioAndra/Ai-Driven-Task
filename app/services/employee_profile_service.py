from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Request, UploadFile
from app.models.employee import Employee
from app.models.skill import Skill
from app.models.EmployeeSkillLink import EmployeeSkillLink
from sqlalchemy import select
import os

UPLOAD_DIR = "Media/employee"
os.makedirs(UPLOAD_DIR, exist_ok=True)


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
            "profile_image": employee.profile_image or ""
        }

    @staticmethod
    def update_employee_profile(
        db: Session,
        employee_id: int,
        update_data: dict,
        request: Request,
        profile_image: UploadFile = None
    ) -> dict:
        employee = db.get(Employee, employee_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found."
            )


        if profile_image:
            file_ext = os.path.splitext(profile_image.filename)[1]
            file_name = f"{employee.email}{file_ext}"
            image_path = os.path.join(UPLOAD_DIR, file_name)

            with open(image_path, "wb") as buffer:
                buffer.write(profile_image.file.read())


            base_url = str(request.base_url).rstrip("/")
            employee.profile_image = f"{base_url}/media/employee/{file_name}"


        for key, value in update_data.items():
            if value is not None:
                setattr(employee, key, value)

        db.add(employee)
        db.commit()
        db.refresh(employee)

        return EmployeeProfileService.get_employee_profile(db, employee.id)
