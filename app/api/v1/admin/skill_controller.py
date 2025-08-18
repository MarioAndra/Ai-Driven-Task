from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.core.database import get_session
from app.schemas.skill import SkillCreate, SkillUpdate
from app.services.skill_service import SkillService
from app.models.skill import Skill
from typing import List


class SkillController:
    @staticmethod
    async def create_skill(skill_data: SkillCreate, db: AsyncSession = Depends(get_session)) -> Skill:
        return await SkillService.create_skill(skill_data, db)

    @staticmethod
    async def update_skill(skill_id: int, skill_data: SkillUpdate, db: AsyncSession = Depends(get_session)) -> Skill:
        return await SkillService.update_skill(skill_id, skill_data, db)

    @staticmethod
    async def delete_skill(skill_id: int, db: AsyncSession = Depends(get_session)) -> None:
        return await SkillService.delete_skill(skill_id, db)

    @staticmethod
    async def list_skills(db: AsyncSession = Depends(get_session)) -> List[Skill]:
        return await SkillService.list_skills(db)
