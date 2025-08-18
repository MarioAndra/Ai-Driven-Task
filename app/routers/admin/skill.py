from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.schemas.skill import SkillCreate, SkillUpdate, SkillRead
# Updated import to use the new controller functions
from app.api.v1.admin import skill_controller

router = APIRouter()

@router.get("/", response_model=List[SkillRead])
async def list_skills(db: AsyncSession = Depends(get_session)):
    return await skill_controller.list_skills_controller(db)

@router.post("/", response_model=SkillRead, status_code=status.HTTP_201_CREATED)
async def create_skill(skill_data: SkillCreate, db: AsyncSession = Depends(get_session)):
    return await skill_controller.create_skill_controller(db, skill_data)

@router.put("/{skill_id}", response_model=SkillRead)
async def update_skill(skill_id: int, skill_data: SkillUpdate, db: AsyncSession = Depends(get_session)):
    return await skill_controller.update_skill_controller(db, skill_id, skill_data)

@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill(skill_id: int, db: AsyncSession = Depends(get_session)):
    await skill_controller.delete_skill_controller(db, skill_id)

    return None