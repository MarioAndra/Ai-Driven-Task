from fastapi import APIRouter, Depends, Request
from sqlmodel import Session
from app.core.database import get_session
from app.schemas.auth import RegisterRequestForm
from app.api.v1.employee.auth.register_controller import register_controller

router = APIRouter()

@router.post("/register")
def register(
    request_data: dict = Depends(RegisterRequestForm),
    session: Session = Depends(get_session),
    request: Request = None
):
    return register_controller(session, request_data, request)
