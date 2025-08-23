# app/api/v1/employee/employee_controller.py
from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.database import get_session
from app.services.employee_skill_service import EmployeeSkillService
from app.core.security import get_current_employee
from app.models.employee import Employee
from app.schemas.employee_skill import EmployeeSkillCreate
from app.schemas.employee import EmployeeProfile, EmployeeUpdateRequest
from app.services.employee_profile import EmployeeProfileService
from app.services.employee_update_service import EmployeeUpdateService
from app.schemas.employee import TaskSummaryResponse


class EmployeeController:
    @staticmethod
    def get_my_skills(
        db: Session,
        current_employee: Employee
    ):
        return EmployeeSkillService.get_employee_skills(current_employee.id, db)
    
    @staticmethod
    def add_employee_skill(
        employee_id: int,
        skill_data: EmployeeSkillCreate,
        db: Session = Depends(get_session),
        
    ):
        
       return EmployeeSkillService.add_employee_skill(employee_id, skill_data, db)
    
    @staticmethod
    def get_my_profile(
        db: Session,
        current_employee: Employee
    ):
        return EmployeeProfileService.get_employee_profile(db, current_employee.id)
  
    @staticmethod
    def update_my_profile(
        db: Session,
        current_employee: Employee,
        update_data: EmployeeUpdateRequest
    ):
        return EmployeeUpdateService.update_employee_profile(db, current_employee.id, update_data)
   


