import os
from sqlmodel import Session
from fastapi import Request
from app.services.auth_service import register_employee, generate_token
from app.schemas.auth import RegisterRequest


def register_controller(session: Session, request_data: RegisterRequest):


    employee = register_employee(
        session,

        **request_data.dict()
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