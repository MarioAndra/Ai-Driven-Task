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
        available_hours=request.available_hours
    )


    token = generate_token(employee)


    return {
        "message": "Employee registered successfully.",
        "employee": employee,
        "access_token": token
    }