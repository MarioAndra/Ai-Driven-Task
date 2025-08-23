from pydantic import BaseModel
from enum import Enum

class SubtaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class SubtaskUpdateRequest(BaseModel):
    status: SubtaskStatus
