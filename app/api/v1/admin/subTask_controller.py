
from sqlalchemy.orm import Session
from app.services.subTask_service import SubTaskService

class SubTaskController:
    @staticmethod
    def create(db: Session, assignment_data: dict):
        return SubTaskService.create_assignment(db, assignment_data)

    @staticmethod
    def update(db: Session, assignment_id: int, update_data: dict):
        return SubTaskService.update_assignment(db, assignment_id, update_data)

    @staticmethod
    def delete(db: Session, assignment_id: int):
        return SubTaskService.delete_assignment(db, assignment_id)
