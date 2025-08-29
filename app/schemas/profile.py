from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class SkillResponse(BaseModel):
    skill_id: int
    name: str
    rating: int

    class Config:
        orm_mode = True


class EmployeeProfileResponse(BaseModel):
    id: int
    name: str
    email: str
    phone_number: Optional[str] = None
    address: Optional[str] = None
    birth_date: Optional[date] = None
    skills: List[SkillResponse]
    task_capacity: Optional[int] = None
    available_hours: Optional[int] = None
    profile_image: Optional[str] = ""

    class Config:
        orm_mode = True
