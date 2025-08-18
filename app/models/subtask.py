from typing import List, Optional
from sqlmodel import Field, Relationship
from .base import TimeStampedModel

class Subtask(TimeStampedModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str
    is_assigned: bool = False

    task_id: Optional[int] = Field(default=None, foreign_key="task.id")

    parent_task: Optional["Task"] = Relationship(back_populates="subtasks")
    assignments: List["Assignment"] = Relationship(back_populates="subtask")
