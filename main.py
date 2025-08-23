from fastapi import FastAPI
from app.core.database import create_db_and_tables
from app.routers.auth import router as auth_router
from app.routers.admin.auth import router as auth_router_admin
from app.routers.admin import router as admin_router
from app.routers.employee.employee import router as employee_router
from app.routers.employee import employee
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.requests import Request
import traceback

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])



#admin section
app.include_router(auth_router_admin, prefix="/api/v1/admin/auth", tags=["Auth-admin"])
app.include_router(
    admin_router,
    prefix="/api/v1/admin"

)
#employee section
app.include_router(employee_router, prefix="/api/v1", tags=["Employee"])

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print("EXCEPTION TRACEBACK:")
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )