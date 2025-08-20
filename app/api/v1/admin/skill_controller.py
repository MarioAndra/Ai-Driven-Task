from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.database import get_session
from app.schemas.skill import SkillCreate, SkillUpdate
from app.services.skill_service import SkillService
from app.models.skill import Skill
from typing import List


class SkillController:
    @staticmethod
    def create_skill(skill_data: SkillCreate, db: Session = Depends(get_session)) -> Skill:
        return SkillService.create_skill(skill_data, db)

    @staticmethod
    def update_skill(skill_id: int, skill_data: SkillUpdate, db: Session = Depends(get_session)) -> Skill:
        return SkillService.update_skill(skill_id, skill_data, db)

    @staticmethod
    def delete_skill(skill_id: int, db: Session = Depends(get_session)) -> None:
        return SkillService.delete_skill(skill_id, db)

    @staticmethod
    def list_skills(db: Session = Depends(get_session)) -> List[Skill]:
        return SkillService.list_skills(db)
