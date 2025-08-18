from fastapi import APIRouter
from typing import List
from app.api.v1.admin.employee_skill_controller import EmployeeSkillController
from app.schemas.employee_skill import EmployeeSkillCreate, EmployeeSkillUpdate, EmployeeSkillRead

router = APIRouter(prefix="/employee-skills", tags=["Admin - Employee Skills"])


@router.get("/{employee_id}", response_model=List[EmployeeSkillRead])
async def get_employee_skills(employee_id: int):
    return await EmployeeSkillController.get_employee_skills(employee_id)


@router.post("/{employee_id}")
async def add_employee_skill(employee_id: int, skill_data: EmployeeSkillCreate):
    return await EmployeeSkillController.add_employee_skill(employee_id, skill_data)


@router.put("/{employee_id}/{skill_id}")
async def update_employee_skill(employee_id: int, skill_id: int, skill_data: EmployeeSkillUpdate):
    return await EmployeeSkillController.update_employee_skill(employee_id, skill_id, skill_data)


@router.delete("/{employee_id}/{skill_id}")
async def delete_employee_skill(employee_id: int, skill_id: int):
    return await EmployeeSkillController.delete_employee_skill(employee_id, skill_id)
