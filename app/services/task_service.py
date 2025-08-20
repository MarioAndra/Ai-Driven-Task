from sqlalchemy.orm import Session
from sqlalchemy.future import select
from fastapi import HTTPException

from app.models.task import Task
from app.models.subtask import Subtask
from app.models.Assignment import Assignment


class TaskService:
    @staticmethod
    def index(db: Session):
        """عرض جميع المهام مع السب تاكس"""
        result = db.execute(select(Task).options())
        tasks = result.scalars().all()
        return tasks

    @staticmethod
    def show(task_id: int, db: Session, status: str | None = None):
        result = db.execute(select(Task).where(Task.id == task_id))
        task = result.scalars().first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        # جلب السب تاكس الخاصة بهالتاسك
        subtasks_query = select(Subtask).where(Subtask.task_id == task_id)
        if status:
            subtasks_query = subtasks_query.where(Subtask.status == status)

        subtasks = db.execute(subtasks_query).scalars().all()

        # تجهيز الريسبونس مع الموظف المستلم
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
        """حذف تاسك مع كل سب تاكس و إلغاء الربط بالـ assignments"""
        result = db.execute(select(Task).where(Task.id == task_id))
        task = result.scalars().first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        # جلب كل السب تاكس
        subtasks = db.execute(select(Subtask).where(Subtask.task_id == task_id)).scalars().all()

        for sub in subtasks:
            # حذف كل الـ assignments المرتبطة بالسب تاكس
            assignments = db.execute(select(Assignment).where(Assignment.sub_task_id == sub.id)).scalars().all()
            for a in assignments:
                db.delete(a)
            db.delete(sub)

        db.delete(task)
        db.commit()
        return {"detail": "Task and related subtasks/assignments deleted successfully"}

    @staticmethod
    def update(task_id: int, description: str, db: Session):
        """تعديل الوصف للتاسك"""
        result = db.execute(select(Task).where(Task.id == task_id))
        task = result.scalars().first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        task.description = description
        db.add(task)
        db.commit()
        db.refresh(task)
        return {"detail": "Task updated successfully", "task": task}
