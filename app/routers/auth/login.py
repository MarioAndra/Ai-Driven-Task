from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.schemas.auth import LoginRequest
from app.api.v1.employee.auth.login_controller import login_controller

router = APIRouter()

@router.post("/login")
def login(request: LoginRequest, session: Session = Depends(get_session)):
    return login_controller(session, request.email, request.password)
