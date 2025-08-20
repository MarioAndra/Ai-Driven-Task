from sqlmodel import Session
from app.schemas.auth import RegisterRequest
from app.services.auth_service import register_employee, generate_token




def register_controller(session: Session, request: RegisterRequest):
    employee = register_employee(
        session,
        name=request.name,
        email=request.email,
        password=request.password,
        task_capacity=request.task_capacity,
        available_hours=request.available_hours,
        phone_number=request.phone_number,
        address=request.address,
        birth_date=request.birth_date,
    )

    token = generate_token(employee)

    return {
        "message": "Employee registered successfully.",
        "employee": {
            "id": employee.id,
            "name": employee.name,
            "email": employee.email,
            "role": employee.role,
            "status": employee.status,
            "task_capacity": employee.task_capacity,
            "available_hours": employee.available_hours,
            "phone_number": employee.phone_number,
            "address": employee.address,
            "birth_date": employee.birth_date,
        },
        "access_token": token,
    }
