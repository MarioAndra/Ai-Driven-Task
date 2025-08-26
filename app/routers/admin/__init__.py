from fastapi import APIRouter
from .employee import router as employee_router
from .skill import router as skill_router
from .employee_skill import router as employee_skill_router
from .task import router as task_router
# --- 1. Import the new assignment router ---
from .assignment import router as assignment_router
from .subtask import router as subTask_router

router = APIRouter()

router.include_router(
    employee_router,
    prefix="/employees",
    tags=["Admin - Employees"]
)
router.include_router(
    skill_router,
    prefix="/skills",
    tags=["Admin - Skills"]
)
router.include_router(
    employee_skill_router,
    prefix="/employee-skills",
    tags=["Admin - Employee - Skills"]
)

router.include_router(
    task_router,
    prefix="/tasks",
    tags=["Admin - Tasks"]
)


router.include_router(
    assignment_router,
    prefix="/assignments",
    tags=["Admin - Assignments"]
)


router.include_router(
    subTask_router,
    prefix="/subTasks",
    tags=["Admin - Assignments SubTask"]
)
