from typing import List, Optional
from sqlmodel import Field, Relationship
from .base import TimeStampedModel
from enum import Enum

class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class Task(TimeStampedModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str
    status: TaskStatus = Field(default=TaskStatus.pending)
    employee_id: Optional[int] = Field(default=None, foreign_key="employee.id")

    subtasks: List["Subtask"] = Relationship(back_populates="parent_task")
