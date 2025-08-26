from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.api.v1.admin.assignment_controller import AssignmentController
from app.schemas.assignment import FeedbackPayload

router = APIRouter()

@router.post("/{assignment_id}/feedback")
def submit_feedback(assignment_id: int, payload: FeedbackPayload, db: Session = Depends(get_session)):
    return AssignmentController.submit_feedback(assignment_id, payload.rating, db)