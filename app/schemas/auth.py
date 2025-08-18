from pydantic import BaseModel, EmailStr
from typing import Optional

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    task_capacity: Optional[int] = None
    available_hours: Optional[int] = None
