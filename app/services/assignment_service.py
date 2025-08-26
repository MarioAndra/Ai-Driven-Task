from sqlmodel import Session, select
from fastapi import HTTPException

from app.models.Assignment import Assignment
from app.ai import task_assessor


class AssignmentService:
    @staticmethod
    def submit_feedback_and_evolve(assignment_id: int, rating: int, db: Session):

        assignment = db.get(Assignment, assignment_id)
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")


        assignment.feedback = str(rating)
        db.add(assignment)
        db.commit()


        training_statement = select(Assignment).where(Assignment.feedback != None)
        all_rated_assignments = db.exec(training_statement).all()


        db_history = []
        for a in all_rated_assignments:

            features = {
                "match_score": a.match_score if a.match_score is not None else 0.0,
                "avg_skill_level": a.avg_skill_level if a.avg_skill_level is not None else 0.0,
                "availability": a.availability if a.availability is not None else 0.0,
                "current_load": a.current_load if a.current_load is not None else 0.0
            }
            db_history.append({
                "features": features,
                "feedback": int(a.feedback)
            })


        current_weights = task_assessor.load_model_weights()
        task_assessor.evolve_model_from_db_history(db_history, current_weights)

        return {"message": "Feedback saved and model training initiated."}
