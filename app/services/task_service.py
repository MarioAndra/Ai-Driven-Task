from sqlalchemy.orm import Session
from sqlalchemy.future import select
from fastapi import HTTPException, BackgroundTasks
from app.models.task import Task
from app.models.subtask import Subtask
from app.models.Assignment import Assignment
from app.schemas.task import TaskCreate, AnswersPayload
from app.ai import task_assessor
from app.services.ai_service import AIService

class TaskService:

    @staticmethod
    def create_task_and_get_questions(task_in: TaskCreate, db: Session):
        new_task = Task(description=task_in.description)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        prefilled_details = task_assessor.extract_details_from_description(new_task.description)
        questions = task_assessor.generate_questions(new_task.description, prefilled_details)

        return {"task": new_task, "prefilled_details": prefilled_details, "questions": questions}

    @staticmethod
    def generate_and_assign_subtasks(task_id: int, payload: AnswersPayload, db: Session, background_tasks: BackgroundTasks):
        print("-> [TaskService] Trying to build subtasks...", flush=True)
        subtask_descriptions = task_assessor.build_subtasks_from_answers(
            payload.answers,
            payload.prefilled_details
        )
        print("-> [TaskService] Subtasks built successfully.", flush=True)

        new_subtasks = []
        for desc in subtask_descriptions:
            subtask = Subtask(description=desc, task_id=task_id)
            db.add(subtask)
            new_subtasks.append(subtask)
        db.commit()

        for st in new_subtasks:
            db.refresh(st)


        assignments = AIService.get_assignments_for_tasks(db, new_subtasks, background_tasks)
        return assignments

    @staticmethod
    def index(db: Session):
        result = db.execute(select(Task).options())
        tasks = result.scalars().all()
        return tasks

    @staticmethod
    def show(task_id: int, db: Session, status: str | None = None):
        result = db.execute(select(Task).where(Task.id == task_id))
        task = result.scalars().first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        subtasks_query = select(Subtask).where(Subtask.task_id == task_id)
        if status:
            subtasks_query = subtasks_query.where(Subtask.status == status)

        subtasks = db.execute(subtasks_query).scalars().all()

        subtasks_data = []
        for sub in subtasks:
            subtasks_data.append({
                "id": sub.id,
                "description": sub.description,
                "status": sub.status,
                "assigned_employee": sub.assigned_employee
            })

        return {
            "task": {
                "id": task.id,
                "description": task.description,
                "created_at": task.created_at,
                "updated_at": task.updated_at,
            },
            "subtasks": subtasks_data
        }

    @staticmethod
    def delete(task_id: int, db: Session):
        result = db.execute(select(Task).where(Task.id == task_id))
        task = result.scalars().first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        subtasks = db.execute(select(Subtask).where(Subtask.task_id == task_id)).scalars().all()
        for sub in subtasks:
            assignments = db.execute(select(Assignment).where(Assignment.sub_task_id == sub.id)).scalars().all()
            for a in assignments:
                db.delete(a)
            db.delete(sub)

        db.delete(task)
        db.commit()
        return {"detail": "Task and related subtasks/assignments deleted successfully"}

    @staticmethod
    def update(task_id: int, description: str, db: Session):
        result = db.execute(select(Task).where(Task.id == task_id))
        task = result.scalars().first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        task.description = description
        db.add(task)
        db.commit()
        db.refresh(task)
        return {"detail": "Task updated successfully", "task": task}
