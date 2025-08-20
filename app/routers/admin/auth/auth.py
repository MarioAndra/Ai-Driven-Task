# app/api/v1/admin/admin_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.api.v1.admin.auth.Login_Controller import login
from app.schemas.auth import LoginRequest
router = APIRouter()

@router.post("/login")
def login_admin(request: LoginRequest, session: Session = Depends(get_session)):
    return login(session, request.email, request.password)
