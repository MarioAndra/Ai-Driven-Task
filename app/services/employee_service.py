from typing import List, Optional
from sqlmodel import Session, select

from app.models.employee import Employee, EmployeeStatus
# تعديل: استيراد النموذج من ملف schemas
from app.schemas.employee import EmployeeUpdateRequest


def get_all_employees(session: Session, status: Optional[EmployeeStatus] = None) -> List[Employee]:
    query = select(Employee)
    if status:
        query = query.where(Employee.status == status)

    employees = session.exec(query).all()
    return employees


def get_employee_by_id(session: Session, employee_id: int) -> Optional[Employee]:
    employee = session.get(Employee, employee_id)
    return employee


def update_employee_details(session: Session, employee: Employee, update_data: EmployeeUpdateRequest) -> Employee:
    update_dict = update_data.model_dump(exclude_unset=True)

    if not update_dict:
        return employee

    for key, value in update_dict.items():
        setattr(employee, key, value)

    session.add(employee)
    session.commit()
    session.refresh(employee)

    return employee
