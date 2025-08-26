from pydantic import BaseModel, EmailStr
from typing import List, Optional
from app.models.employee import EmployeeStatus
from datetime import date


class SkillDetail(BaseModel):
    id: int
    name: str
    rating: int

    class Config:
        orm_mode = True


class EmployeeProfile(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone_number: Optional[str] = None
    address: Optional[str] = None
    birth_date: Optional[date] = None
    skills: List[SkillDetail]
    task_capacity: int
    available_hours: int

    class Config:
        orm_mode = True


class EmployeeUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    status: Optional[EmployeeStatus] = None
    task_capacity: Optional[int] = None
    available_hours: Optional[int] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    birth_date: Optional[date] = None
