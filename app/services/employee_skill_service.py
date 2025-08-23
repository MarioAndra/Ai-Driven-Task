from sqlalchemy.orm import Session
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.employee import Employee
from app.models.skill import Skill
from app.models.EmployeeSkillLink import EmployeeSkillLink
from app.schemas.employee_skill import EmployeeSkillCreate, EmployeeSkillUpdate, EmployeeSkillRead


class EmployeeSkillService:
    @staticmethod
    def get_employee_skills(employee_id: int, db: Session) -> list[EmployeeSkillRead]:
        """
        Retrieves a list of skills and ratings for a given employee,
        and returns them as a list of EmployeeSkillRead Pydantic models.
        """
        
        result = db.execute(
            select(Skill.id, Skill.name, EmployeeSkillLink.rating)
            .join(EmployeeSkillLink, Skill.id == EmployeeSkillLink.skill_id)
            .where(EmployeeSkillLink.employee_id == employee_id)
        )
        
        # We process the result into a list of Pydantic models.
        # This ensures the data matches the expected schema and avoids validation errors.
        skills = [
            EmployeeSkillRead(id=s[0], name=s[1], rating=s[2]) 
            for s in result.all()
        ]
        return skills
#####################################################################################################
    @staticmethod
    def add_employee_skill(employee_id: int, skill_data: EmployeeSkillCreate, db: Session):
        emp_result = db.execute(select(Employee).where(Employee.id == employee_id))
        employee = emp_result.scalars().first()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        skill_result = db.execute(select(Skill).where(Skill.id == skill_data.skill_id))
        skill = skill_result.scalars().first()
        if not skill:
            raise HTTPException(status_code=404, detail="Skill not found")

        link_result = db.execute(
            select(EmployeeSkillLink).where(
                EmployeeSkillLink.employee_id == employee_id,
                EmployeeSkillLink.skill_id == skill_data.skill_id
            )
        )
        link = link_result.scalars().first()
        if link:
            raise HTTPException(status_code=400, detail="Skill already assigned to employee")

        new_link = EmployeeSkillLink(
            employee_id=employee_id,
            skill_id=skill_data.skill_id,
            rating=skill_data.rating
        )
        db.add(new_link)
        db.commit()
        return {"detail": "Skill added to employee successfully"}
##############################################################################################
    @staticmethod
    def update_employee_skill(employee_id: int, skill_id: int, skill_data: EmployeeSkillUpdate, db: Session):
        result = db.execute(
            select(EmployeeSkillLink).where(
                EmployeeSkillLink.employee_id == employee_id,
                EmployeeSkillLink.skill_id == skill_id
            )
        )
        link = result.scalars().first()
        if not link:
            raise HTTPException(status_code=404, detail="Employee skill not found")

        if skill_data.rating is not None:
            link.rating = skill_data.rating

        db.add(link)
        db.commit()
        db.refresh(link)
        return {"detail": "Skill rating updated successfully"}

    @staticmethod
    def delete_employee_skill(employee_id: int, skill_id: int, db: Session):
        result = db.execute(
            select(EmployeeSkillLink).where(
                EmployeeSkillLink.employee_id == employee_id,
                EmployeeSkillLink.skill_id == skill_id
            )
        )
        link = result.scalars().first()
        if not link:
            raise HTTPException(status_code=404, detail="Employee skill not found")

        db.delete(link)
        db.commit()
        return {"detail": "Skill removed from employee successfully"}
