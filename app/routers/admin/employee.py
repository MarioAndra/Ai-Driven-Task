from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.database import get_session
from app.models.employee import Employee, EmployeeStatus


from app.schemas.employee import (
    EmployeeUpdateRequest,
    EmployeeDetailsResponse
)

from app.api.v1.admin.employee_controller import (
    index_employees_controller,
    show_employee_controller,
    update_employee_controller,
)


router = APIRouter()

@router.get("/", response_model=List[Employee])
def get_all_employees(status: Optional[EmployeeStatus] = None, session: Session = Depends(get_session)):
    return index_employees_controller(session, status)


@router.get("/{employee_id}", response_model=EmployeeDetailsResponse)
def get_employee_details(employee_id: int, session: Session = Depends(get_session)):
    return show_employee_controller(session, employee_id)


@router.patch("/{employee_id}", response_model=Employee)
def partial_update_employee(employee_id: int, request: EmployeeUpdateRequest, session: Session = Depends(get_session)):
    return update_employee_controller(session, employee_id, request)
