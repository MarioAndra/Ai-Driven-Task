from fastapi import APIRouter
from .employee import router as employee_router

router = APIRouter()

# أضف الـ prefix والـ tags هنا
router.include_router(
    employee_router, 
    prefix="/employees", 
    tags=["Admin - Employees"]
)

# في المستقبل، يمكنك إضافة راوترات أخرى بنفس الطريقة
# from .tasks import router as tasks_router
# router.include_router(tasks_router, prefix="/tasks", tags=["Admin - Tasks"])
