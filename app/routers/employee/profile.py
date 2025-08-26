from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.api.v1.employee.employee_profile_controller import EmployeeProfileController
from app.core.security import get_current_employee
from app.models.employee import Employee

router = APIRouter(
    prefix="/profile",
    tags=["Employee Profile"]
)

@router.get(
    "/",
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
    status_code=status.HTTP_200_OK,
    summary="Update current employee's profile"
)
def update_employee_profile_endpoint(
    update_data: dict,
    db: Session = Depends(get_session),
    current_employee: Employee = Depends(get_current_employee)
):
    return EmployeeProfileController.update_my_profile(db, current_employee, update_data)
