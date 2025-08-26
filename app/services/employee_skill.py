
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.skill import Skill
from app.models.EmployeeSkillLink import EmployeeSkillLink


class EmployeeSkillService:
    @staticmethod
    def get_employee_skills(db: Session, employee_id: int) -> list[dict]:

        stmt = (
            select(Skill.id, Skill.name, EmployeeSkillLink.rating)
            .join(EmployeeSkillLink, Skill.id == EmployeeSkillLink.skill_id)
            .where(EmployeeSkillLink.employee_id == employee_id)
        )
        results = db.execute(stmt).all()

        skills_list = [
            {"skill_id": r.id, "name": r.name, "rating": r.rating} for r in results
        ]
        return skills_list

    @staticmethod
    def add_employee_skill(db: Session, employee_id: int, skill_data: dict):

        skill_id = skill_data.get("skill_id")
        rating = skill_data.get("rating")

        if not skill_id or rating is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Skill ID and rating are required."
            )


        skill = db.get(Skill, skill_id)
        if not skill:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Skill with id {skill_id} not found."
            )


        link = db.get(EmployeeSkillLink, (employee_id, skill.id))

        if link:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Skill '{skill.name}' already exists for this employee."
            )

        new_link = EmployeeSkillLink(employee_id=employee_id, skill_id=skill.id, rating=rating)
        db.add(new_link)
        db.commit()
        return {"message": "Skill added successfully.", "skill_id": skill.id, "name": skill.name, "rating": rating}

    @staticmethod
    def update_employee_skill(db: Session, employee_id: int, skill_id: int, update_data: dict):

        new_rating = update_data.get("rating")
        if new_rating is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rating is required."
            )

        link = db.get(EmployeeSkillLink, (employee_id, skill_id))

        if not link:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill not found for this employee."
            )

        link.rating = new_rating
        db.add(link)
        db.commit()

        skill = db.get(Skill, skill_id)
        return {"message": "Skill updated successfully.", "skill_id": skill.id, "name": skill.name,
                "rating": new_rating}

    @staticmethod
    def delete_employee_skill(db: Session, employee_id: int, skill_id: int):

        link = db.get(EmployeeSkillLink, (employee_id, skill_id))

        if not link:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill not found for this employee."
            )

        db.delete(link)
        db.commit()
        return {"message": "Skill deleted successfully."}
