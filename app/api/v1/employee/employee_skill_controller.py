# app/controllers/employee_skill_controller.py
from sqlalchemy.orm import Session
from app.services.employee_skill import EmployeeSkillService
from app.models.employee import Employee


class EmployeeSkillController:
    @staticmethod
    def get_my_skills(db: Session, current_employee: Employee):
        return EmployeeSkillService.get_employee_skills(db, current_employee.id)

    @staticmethod
    def add_my_skill(db: Session, current_employee: Employee, skill_data: dict):
        return EmployeeSkillService.add_employee_skill(db, current_employee.id, skill_data)

    @staticmethod
    def update_my_skill(db: Session, current_employee: Employee, skill_id: int, update_data: dict):
        return EmployeeSkillService.update_employee_skill(db, current_employee.id, skill_id, update_data)

    @staticmethod
    def delete_my_skill(db: Session, current_employee: Employee, skill_id: int):
        return EmployeeSkillService.delete_employee_skill(db, current_employee.id, skill_id)
