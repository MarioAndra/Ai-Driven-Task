from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException
from app.models.skill import Skill
from app.schemas.skill import SkillCreate, SkillUpdate
from typing import List


class SkillService:
    @staticmethod
    def create_skill(skill_data: SkillCreate, db: Session) -> Skill:
        new_skill = Skill(name=skill_data.name)
        db.add(new_skill)
        db.commit()
        db.refresh(new_skill)
        return new_skill

    @staticmethod
    def update_skill(skill_id: int, skill_data: SkillUpdate, db: Session) -> Skill:
        result = db.execute(select(Skill).where(Skill.id == skill_id))
        skill = result.scalars().first()
        if not skill:
            raise HTTPException(status_code=404, detail="Skill not found")

        if skill_data.name is not None:
            skill.name = skill_data.name

        db.add(skill)
        db.commit()
        db.refresh(skill)
        return skill

    @staticmethod
    def delete_skill(skill_id: int, db: Session) -> None:
        result = db.execute(select(Skill).where(Skill.id == skill_id))
        skill = result.scalars().first()
        if not skill:
            raise HTTPException(status_code=404, detail="Skill not found")

        db.delete(skill)
        db.commit()
        return None

    @staticmethod
    def list_skills(db: Session) -> List[Skill]:
        result = db.execute(select(Skill))
        return result.scalars().all()
