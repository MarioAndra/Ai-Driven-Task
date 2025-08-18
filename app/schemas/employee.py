from typing import List, Optional
from pydantic import BaseModel
from app.models.employee import Employee, EmployeeStatus


class EmployeeUpdateRequest(BaseModel):
    status: Optional[EmployeeStatus] = None
    task_capacity: Optional[int] = None
    available_hours: Optional[int] = None


class SubtaskResponse(BaseModel):
    id: int
    description: str

class TaskResponse(BaseModel):
    id: int
    description: str

class TaskSummaryResponse(BaseModel):
    parent_task: TaskResponse
    assigned_subtasks: List[SubtaskResponse]

class EmployeeDetailsResponse(BaseModel):
    employee: Employee
    tasks_summary: List[TaskSummaryResponse]

