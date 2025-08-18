from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.skill import Skill
from app.schemas.skill import SkillCreate, SkillUpdate
from typing import List


class SkillService:
    @staticmethod
    async def create_skill(skill_data: SkillCreate, db: AsyncSession) -> Skill:
        new_skill = Skill(name=skill_data.name)
        db.add(new_skill)
        await db.commit()
        await db.refresh(new_skill)
        return new_skill

    @staticmethod
    async def update_skill(skill_id: int, skill_data: SkillUpdate, db: AsyncSession) -> Skill:
        result = await db.execute(select(Skill).where(Skill.id == skill_id))
        skill = result.scalars().first()
        if not skill:
            raise HTTPException(status_code=404, detail="Skill not found")

        if skill_data.name is not None:
            skill.name = skill_data.name

        db.add(skill)
        await db.commit()
        await db.refresh(skill)
        return skill

    @staticmethod
    async def delete_skill(skill_id: int, db: AsyncSession) -> None:
        result = await db.execute(select(Skill).where(Skill.id == skill_id))
        skill = result.scalars().first()
        if not skill:
            raise HTTPException(status_code=404, detail="Skill not found")

        await db.delete(skill)
        await db.commit()
        return None

    @staticmethod
    async def list_skills(db: AsyncSession) -> List[Skill]:
        result = await db.execute(select(Skill))
        return result.scalars().all()
