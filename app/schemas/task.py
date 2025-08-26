from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class TaskCreate(BaseModel):

    description: str

class AnswersPayload(BaseModel):

    answers: Dict[str, str]
    prefilled_details: Dict[str, Any]