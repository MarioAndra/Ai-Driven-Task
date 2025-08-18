from typing import Optional
from sqlmodel import Field
from .base import TimeStampedModel

class EmployeeSkillLink(TimeStampedModel, table=True):
    employee_id: Optional[int] = Field(default=None, foreign_key="employee.id", primary_key=True)
    skill_id: Optional[int] = Field(default=None, foreign_key="skill.id", primary_key=True)
    rating: int
