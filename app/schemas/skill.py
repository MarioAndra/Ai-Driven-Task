from pydantic import BaseModel
from typing import Optional

class SkillBase(BaseModel):
    name: str

class SkillCreate(SkillBase):
    pass

class SkillUpdate(BaseModel):
    name: Optional[str] = None

class SkillRead(SkillBase):
    id: int

    class Config:
        from_attributes = True
