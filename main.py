from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.database import create_db_and_tables, get_session
from app.routers.auth import router as auth_router
from app.routers.admin.auth import router as auth_router_admin
from app.routers.admin import router as admin_router
from app.routers.employee import router as employee_router
from app.core.logging_config import setup_logging
from app.models.skill import Skill
from app.routers.admin import router as subTask_router
from fastapi.staticfiles import StaticFiles
setup_logging()
app = FastAPI()

app.mount("/media/employee", StaticFiles(directory="Media/employee"), name="employee_media")
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Routers
# section employee
app.include_router(employee_router, prefix="/api/v1/employee")
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])

# section admin
app.include_router(auth_router_admin, prefix="/api/v1/admin/auth", tags=["Auth-admin"])
app.include_router(admin_router, prefix="/api/v1/admin")
app.include_router(subTask_router, prefix="/api/v1/admin")

@app.get("/api/v1/skills/", tags=["General Skills"], summary="Get a list of all available skills")
def get_all_skills_endpoint(db: Session = Depends(get_session)):
    skills = db.exec(select(Skill)).scalars().all()
    return [{"id": skill.id, "name": skill.name} for skill in skills]
