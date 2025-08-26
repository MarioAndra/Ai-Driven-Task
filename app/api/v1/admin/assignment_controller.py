from sqlalchemy.orm import Session
from app.services.assignment_service import AssignmentService

class AssignmentController:
    @staticmethod
    def submit_feedback(assignment_id: int, rating: int, db: Session):
        return AssignmentService.submit_feedback_and_evolve(assignment_id, rating, db)