from typing import List, Optional
from sqlmodel import Field, Relationship
from .base import TimeStampedModel
from .EmployeeSkillLink import EmployeeSkillLink

class Skill(TimeStampedModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)

    employees: List["Employee"] = Relationship(back_populates="skills", link_model=EmployeeSkillLink)
