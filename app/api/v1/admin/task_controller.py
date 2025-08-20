from sqlalchemy.orm import Session
from app.services.task_service import TaskService


class TaskController:
    @staticmethod
    def index(db: Session):
        return TaskService.index(db)

    @staticmethod
    def show(task_id: int, db: Session, status: str | None = None):
        return TaskService.show(task_id, db, status)

    @staticmethod
    def delete(task_id: int, db: Session):
        return TaskService.delete(task_id, db)

    @staticmethod
    def update(task_id: int, description: str, db: Session):
        return TaskService.update(task_id, description, db)
