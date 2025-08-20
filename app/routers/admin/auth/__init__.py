from fastapi import APIRouter
from .auth import router as login_router


router = APIRouter()
router.include_router(login_router)

