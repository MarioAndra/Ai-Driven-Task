from typing import List, Optional
from pydantic import BaseModel
from app.models.employee import Employee, EmployeeStatus
from app.schemas.skill import SkillRead 
from app.schemas.employee_skill import EmployeeSkillRead


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


class EmployeeUpdateRequest(BaseModel):
    status: Optional[EmployeeStatus] = None
    task_capacity: Optional[int] = None
    available_hours: Optional[int] = None


class EmployeeSkillsList(BaseModel):
    skills: List[EmployeeSkillRead]


class SkillDetail(BaseModel):
    name: str
    rating: Optional[int] = None

    class Config:
        from_attributes = True


class EmployeeProfile(BaseModel):
    id: int
    name: str
    email: str
    role: str 
    skills: List[SkillDetail]
    task_capacity: Optional[int] = None
    available_hours: Optional[int] = None

    class Config:
        from_attributes = True
