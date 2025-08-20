from sqlalchemy.orm import Session
from app.services.employee_skill_service import EmployeeSkillService
from app.schemas.employee_skill import EmployeeSkillCreate, EmployeeSkillUpdate


class EmployeeSkillController:
    @staticmethod
    def get_employee_skills(employee_id: int, db: Session):
        return EmployeeSkillService.get_employee_skills(employee_id, db)

    @staticmethod
    def add_employee_skill(employee_id: int, skill_data: EmployeeSkillCreate, db: Session):
        return EmployeeSkillService.add_employee_skill(employee_id, skill_data, db)

    @staticmethod
    def update_employee_skill(employee_id: int, skill_id: int, skill_data: EmployeeSkillUpdate, db: Session):
        return EmployeeSkillService.update_employee_skill(employee_id, skill_id, skill_data, db)

    @staticmethod
    def delete_employee_skill(employee_id: int, skill_id: int, db: Session):
        return EmployeeSkillService.delete_employee_skill(employee_id, skill_id, db)
