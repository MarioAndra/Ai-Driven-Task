from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    task_capacity: Optional[int] = None
    available_hours: Optional[int] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    birth_date: Optional[date] = None
