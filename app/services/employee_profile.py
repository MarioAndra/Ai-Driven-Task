from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.employee import Employee
from app.models.skill import Skill
from app.models.EmployeeSkillLink import EmployeeSkillLink
from app.schemas.employee import EmployeeProfile, SkillDetail

class EmployeeProfileService:
    @staticmethod
    def get_employee_profile(db: Session, employee_id: int):
        # جلب بيانات الموظف
        employee = db.execute(select(Employee).where(Employee.id == employee_id)).scalar_one_or_none()
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found."
            )

        # جلب الروابط بين الموظف والمهارات
        employee_skills = db.execute(
            select(EmployeeSkillLink).where(EmployeeSkillLink.employee_id == employee_id)
        ).scalars().all()

        skills_list = []
        for es in employee_skills:
            skill = db.execute(select(Skill).where(Skill.id == es.skill_id)).scalar_one_or_none()
            if skill:
                skills_list.append(SkillDetail(name=skill.name, rating=es.rating))

        # إعادة البيانات بصيغة تتوافق مع EmployeeProfile
        return {
            "id": employee.id,
            "name": employee.name,
            "email": employee.email,
            "role": employee.role, 
            "skills": skills_list,
            "task_capacity": employee.task_capacity,
            "available_hours": employee.available_hours
        }
