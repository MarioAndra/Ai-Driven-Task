from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.core.database import get_session
from app.services.employee_skill_service import EmployeeSkillService
from app.schemas.employee_skill import EmployeeSkillCreate, EmployeeSkillUpdate


class EmployeeSkillController:
    @staticmethod
    async def get_employee_skills(employee_id: int, db: AsyncSession = Depends(get_session)):
        return await EmployeeSkillService.get_employee_skills(employee_id, db)

    @staticmethod
    async def add_employee_skill(employee_id: int, skill_data: EmployeeSkillCreate, db: AsyncSession = Depends(get_session)):
        return await EmployeeSkillService.add_employee_skill(employee_id, skill_data, db)

    @staticmethod
    async def update_employee_skill(employee_id: int, skill_id: int, skill_data: EmployeeSkillUpdate, db: AsyncSession = Depends(get_session)):
        return await EmployeeSkillService.update_employee_skill(employee_id, skill_id, skill_data, db)

    @staticmethod
    async def delete_employee_skill(employee_id: int, skill_id: int, db: AsyncSession = Depends(get_session)):
        return await EmployeeSkillService.delete_employee_skill(employee_id, skill_id, db)
