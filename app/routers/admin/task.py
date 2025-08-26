from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_session
from app.api.v1.admin.task_controller import TaskController

from app.schemas.task import TaskCreate, AnswersPayload
router = APIRouter()


@router.post("/")
def create(task_in: TaskCreate, db: Session = Depends(get_session)):
    return TaskController.create(task_in, db)

@router.post("/{task_id}/process-answers")
async def process_answers(task_id: int, payload: AnswersPayload, db: Session = Depends(get_session)):
    return  TaskController.generate_and_assign_subtasks(task_id, payload, db)

@router.get("/")
def index(db: Session = Depends(get_session)):
    return TaskController.index(db)


@router.get("/{task_id}")
def show(task_id: int, status: Optional[str] = Query(None), db: Session = Depends(get_session)):
    return TaskController.show(task_id, db, status)


@router.delete("/{task_id}")
def delete(task_id: int, db: Session = Depends(get_session)):
    return TaskController.delete(task_id, db)


@router.put("/{task_id}")
def update(task_id: int, description: str, db: Session = Depends(get_session)):
    return TaskController.update(task_id, description, db)