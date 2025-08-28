from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
from fastapi import Form, File, UploadFile



class LoginRequest(BaseModel):
    email: EmailStr
    password: str



def RegisterRequestForm(
    name: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...),
    task_capacity: Optional[int] = Form(None),
    available_hours: Optional[int] = Form(None),
    phone_number: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    birth_date: Optional[date] = Form(None),
    profile_image: Optional[UploadFile] = File(None)
):
    return {
        "name": name,
        "email": email,
        "password": password,
        "task_capacity": task_capacity,
        "available_hours": available_hours,
        "phone_number": phone_number,
        "address": address,
        "birth_date": birth_date,
        "profile_image": profile_image,
    }
