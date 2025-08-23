from pydantic import BaseModel
from typing import Optional

class EmployeeSkillBase(BaseModel):
    skill_id: int
    rating: int

class EmployeeSkillCreate(EmployeeSkillBase):
    pass

class EmployeeSkillUpdate(BaseModel):
    rating: Optional[int] = None

class EmployeeSkillRead(BaseModel):
    id: int
    name: str
    rating: int

    class Config:
        from_attributes = True 
