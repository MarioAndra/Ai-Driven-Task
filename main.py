from fastapi import FastAPI
from app.core.database import create_db_and_tables
from app.routers.auth import router as auth_router
from app.routers.admin import router as admin_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])

app.include_router(
    admin_router,
    prefix="/api/v1/admin"
)
