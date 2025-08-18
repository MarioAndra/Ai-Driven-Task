from fastapi import HTTPException
from sqlmodel import Session
from app.services.auth_service import authenticate_employee, generate_token

def login_controller(session: Session, email: str, password: str):
    employee = authenticate_employee(session, email, password)
    if not employee:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = generate_token(employee)
    return {
        "message": "Employee logged in successfully.",
        "employee": employee,
        "access_token": token
    }
