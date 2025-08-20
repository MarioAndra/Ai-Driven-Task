from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.schemas.skill import SkillCreate, SkillUpdate, SkillRead
from app.api.v1.admin.skill_controller import SkillController

router = APIRouter()

@router.get("/", response_model=List[SkillRead])
def list_skills(db: Session = Depends(get_session)):
    return SkillController.list_skills(db)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_skill(skill_data: SkillCreate, db: Session = Depends(get_session)):
    skill = SkillController.create_skill(skill_data, db)
    return {"message": "Created Done Successfully ", "data": skill}

@router.put("/{skill_id}")
def update_skill(skill_id: int, skill_data: SkillUpdate, db: Session = Depends(get_session)):
    skill = SkillController.update_skill(skill_id, skill_data, db)
    return {"message": "Updated Done Successfully ", "data": skill}

@router.delete("/{skill_id}")
def delete_skill(skill_id: int, db: Session = Depends(get_session)):
    SkillController.delete_skill(skill_id, db)
    return {"message": "Deleted Done Successfully "}
