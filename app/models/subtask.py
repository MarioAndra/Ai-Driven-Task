from typing import List, Optional
from sqlmodel import Field, Relationship
from .base import TimeStampedModel
from sqlalchemy import Column, Enum as SQLAlchemyEnum
import enum

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class SubtaskStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class Subtask(TimeStampedModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str
    status: SubtaskStatus = Field(default=SubtaskStatus.pending)

    task_id: Optional[int] = Field(default=None, foreign_key="task.id")

    parent_task: Optional["Task"] = Relationship(back_populates="subtasks")
    assignments: List["Assignment"] = Relationship(back_populates="subtask")

    @property
    def assigned_employee(self):
        if self.assignments and len(self.assignments) > 0:
            return self.assignments[0].employee.name if self.assignments[0].employee else "N/A"
        return "N/A"

