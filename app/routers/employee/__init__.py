
from fastapi import APIRouter
from .profile import router as profile_router
from .skill import router as skill_router

from .task import router as task_router

router = APIRouter()

router.include_router(profile_router)
router.include_router(skill_router)
router.include_router(task_router)
