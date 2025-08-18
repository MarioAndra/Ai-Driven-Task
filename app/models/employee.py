from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, Enum as SQLAlchemyEnum
import enum
from sqlalchemy import Column, String
from .base import TimeStampedModel
from .EmployeeSkillLink import EmployeeSkillLink


class EmployeeStatus(str, enum.Enum):
    available = "available"
    unavailable = "unavailable"


class Employee(TimeStampedModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True, nullable=False)
    password: str
    role: str = Field(default="employee", max_length=50)
    status: EmployeeStatus = Field(
        default=EmployeeStatus.available,
        sa_column=Column(SQLAlchemyEnum(EmployeeStatus), nullable=False)
    )

    task_capacity: Optional[int] = None
    available_hours: Optional[int] = None

    assignments: List["Assignment"] = Relationship(back_populates="employee")
    skills: List["Skill"] = Relationship(back_populates="employees", link_model=EmployeeSkillLink)
