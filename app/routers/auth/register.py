from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.schemas.auth import RegisterRequest

from app.api.v1.employee.auth.register_controller import register_controller

router = APIRouter()

@router.post("/register")
def register(request: RegisterRequest, session: Session = Depends(get_session)):

    return register_controller(session, request)