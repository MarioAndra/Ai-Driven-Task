from sqlmodel import Session
from app.models.employee import Employee, EmployeeStatus
from app.models.Admin import Admin
from app.core.security import verify_password, hash_password, create_access_token
from datetime import timedelta
from typing import Union
from datetime import date
def authenticate_employee(session: Session, email: str, password: str):
    employee = session.query(Employee).filter(Employee.email == email).first()
    if not employee or not verify_password(password, employee.password):
        return None
    return employee

def register_employee(
    session: Session,
    name: str,
    email: str,
    password: str,
    task_capacity: int = None,
    available_hours: int = None,
    phone_number: str = None,
    address: str = None,
    birth_date: date = None
):
    existing = session.query(Employee).filter(Employee.email == email).first()
    if existing:
        raise ValueError("Email already registered.")

    hashed_pw = hash_password(password)
    employee = Employee(
        name=name,
        email=email,
        password=hashed_pw,
        task_capacity=task_capacity,
        available_hours=available_hours,
        phone_number=phone_number,
        address=address,
        birth_date=birth_date,
        status=EmployeeStatus.available,
        role="employee",
    )
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee

def authenticate_admin(session: Session, email: str, password: str):
    admin = session.query(Admin).filter(Admin.email == email).first()
    if not admin or not verify_password(password, admin.password):
        return None
    return admin

def generate_token(user: Union[Employee, Admin]):

    payload = {
        "sub": str(user.id),
        "email": user.email,
        "role": user.role
    }
    return create_access_token(payload, timedelta(minutes=60))