from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from pydantic import BaseModel, EmailStr

from app.core.database import get_session
from app.api.v1.employee.employee_profile_controller import EmployeeProfileController
from app.core.security import get_current_employee
from app.models.employee import Employee
from app.schemas.profile import EmployeeProfileResponse

router = APIRouter(
    prefix="/profile",
    tags=["Employee Profile"]
)


class EmployeeProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    task_capacity: Optional[int] = None
    available_hours: Optional[int] = None
    birth_date: Optional[date] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    status: Optional[str] = None


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
    update_data: EmployeeProfileUpdateRequest,
    db: Session = Depends(get_session),
    current_employee: Employee = Depends(get_current_employee)
):
    return EmployeeProfileController.update_my_profile(
        db, current_employee, update_data.dict(), request
    )
