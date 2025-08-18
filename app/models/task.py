from typing import List, Optional
from sqlmodel import Field, Relationship
from .base import TimeStampedModel

class Task(TimeStampedModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str

    subtasks: List["Subtask"] = Relationship(back_populates="parent_task")
