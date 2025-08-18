from typing import Optional
from sqlmodel import Field, Relationship
from .base import TimeStampedModel

class Assignment(TimeStampedModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    match_score: Optional[float] = None
    avg_skill_level: Optional[float] = None
    availability: Optional[int] = None
    current_load: Optional[int] = None
    feedback: Optional[str] = None

    sub_task_id: Optional[int] = Field(default=None, foreign_key="subtask.id")
    employee_id: Optional[int] = Field(default=None, foreign_key="employee.id")

    subtask: Optional["Subtask"] = Relationship(back_populates="assignments")
    employee: Optional["Employee"] = Relationship(back_populates="assignments")
