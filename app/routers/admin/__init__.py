from fastapi import APIRouter
from .employee import router as employee_router
from .skill import router as skill_router
from .employee_skill import router as employee_skill_router  #

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
    tags=["Admin - Employee - Skills"]  # ✅
)
