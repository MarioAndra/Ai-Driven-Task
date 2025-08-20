# app/api/v1/admin/admin_auth_controller.py
from fastapi import HTTPException
from sqlmodel import Session
from app.services.auth_service import authenticate_admin, generate_token

def login(session: Session, email: str, password: str):
    admin = authenticate_admin(session, email, password)
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = generate_token(admin)
    return {
        "message": "Admin logged in successfully.",
        "admin": admin,
        "access_token": token
    }
