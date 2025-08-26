from pydantic import BaseModel
from typing import Optional


class FeedbackPayload(BaseModel):

    rating: int


class AssignmentRead(BaseModel):

    id: int
    sub_task_id: int
    employee_id: int
    match_score: Optional[float]

    class Config:
        from_attributes  = True