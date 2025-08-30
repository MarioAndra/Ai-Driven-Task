from fastapi import APIRouter, Depends, status, Request, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from pydantic import EmailStr

from app.core.database import get_session
from app.api.v1.employee.employee_profile_controller import EmployeeProfileController
from app.core.security import get_current_employee
from app.models.employee import Employee
from app.schemas.profile import EmployeeProfileResponse

router = APIRouter(
    prefix="/profile",
    tags=["Employee Profile"]
)

@router.get(
    "/",
    response_model=EmployeeProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current employee's profile"
)
def get_employee_profile_endpoint(
    db: Session = Depends(get_session),
    current_employee: Employee = Depends(get_current_employee)
):
    return EmployeeProfileController.get_my_profile(db, current_employee)


@router.put(
    "/",
    response_model=EmployeeProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Update current employee's profile"
)
def update_employee_profile_endpoint(
    request: Request,
    db: Session = Depends(get_session),
    current_employee: Employee = Depends(get_current_employee),
    name: Optional[str] = Form(None),
    phone_number: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    task_capacity: Optional[int] = Form(None),
    available_hours: Optional[int] = Form(None),
    birth_date: Optional[date] = Form(None),
    # إضافة حقلي الإيميل وكلمة السر هنا
    email: Optional[EmailStr] = Form(None),
    password: Optional[str] = Form(None),
    profile_image: Optional[UploadFile] = File(None)
):
    update_data = {
        "name": name,
        "phone_number": phone_number,
        "address": address,
        "task_capacity": task_capacity,
        "available_hours": available_hours,
        "birth_date": birth_date,
        "email": email,
        "password": password
    }

    return EmployeeProfileController.update_my_profile(
        db, current_employee, update_data, request, profile_image
    )