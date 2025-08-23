from sqlalchemy.orm import Session
from app.models.task import Task
from app.models.subtask import Subtask
from app.models.Assignment import Assignment
from app.schemas.employee import TaskSummaryResponse, TaskResponse, SubtaskResponse
from fastapi import HTTPException, status
class EmployeeTaskService:
    @staticmethod
    def get_employee_tasks(db: Session, employee_id: int):
        # جلب جميع التعيينات للموظف
        assignments = db.query(Assignment).filter(Assignment.employee_id == employee_id).all()
        
        task_map = {}
        for assign in assignments:
            subtask = assign.subtask
            if not subtask:
                continue
            parent_task = subtask.parent_task
            if not parent_task:
                continue

            # إنشاء أو تحديث المهمة في الخريطة
            if parent_task.id not in task_map:
                task_map[parent_task.id] = {
                    "parent_task": TaskResponse(id=parent_task.id, description=parent_task.description),
                    "assigned_subtasks": []
                }

            task_map[parent_task.id]["assigned_subtasks"].append(
                SubtaskResponse(id=subtask.id, description=f"{subtask.description} ({subtask.status.value})")
            )

        return list(task_map.values())
    
    @staticmethod
    def update_subtask_status(db: Session, employee_id: int, subtask_id: int, new_status: str):
        # تحقق أن الموظف مُعين على هذه المهمة
        assignment = db.query(Assignment).filter(
            Assignment.employee_id == employee_id,
            Assignment.sub_task_id == subtask_id
        ).first()

        if not assignment:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You are not assigned to this subtask.")

        subtask = db.query(Subtask).filter(Subtask.id == subtask_id).first()
        if not subtask:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Subtask not found.")

        subtask.status = new_status
        db.commit()
        db.refresh(subtask)
        return subtask
