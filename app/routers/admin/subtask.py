# app/routers/admin/subtask_router.py
from fastapi import APIRouter, Depends, status, Request,BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.api.v1.admin.subTask_controller import SubTaskController


router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, summary="Assign a subtask to an employee")
async def create_assignment_endpoint(
    request: Request,
    db: Session = Depends(get_session)
):
    assignment_data = await request.json()
    return SubTaskController.create(db, assignment_data)

@router.put("/{assignment_id}", summary="Update (re-assign) a subtask")
async def update_assignment_endpoint(
    assignment_id: int,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_session)
):
    update_data = await request.json()
    return SubTaskController.update(db, assignment_id, update_data, background_tasks)

@router.delete("/{assignment_id}", summary="Delete an assignment (un-assign a subtask)")
def delete_assignment_endpoint(
    assignment_id: int,
    db: Session = Depends(get_session)
):
    return SubTaskController.delete(db, assignment_id)
