from sqlalchemy.orm import Session
from app.services.task_service import TaskService
from app.schemas.task import TaskCreate, AnswersPayload

class TaskController:

    @staticmethod
    def create(task_in: TaskCreate, db: Session):
        return TaskService.create_task_and_get_questions(task_in, db)

    @staticmethod
    def generate_and_assign_subtasks(task_id: int, payload: AnswersPayload, db: Session):
        return TaskService.generate_and_assign_subtasks(task_id, payload, db)

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
