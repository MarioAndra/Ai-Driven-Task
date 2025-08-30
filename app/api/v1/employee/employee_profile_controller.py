from sqlalchemy.orm import Session
from fastapi import Request
from app.services.employee_profile_service import EmployeeProfileService
from app.models.employee import Employee


class EmployeeProfileController:
    @staticmethod
    def get_my_profile(db: Session, current_employee: Employee) -> dict:
        return EmployeeProfileService.get_employee_profile(db, current_employee.id)

    @staticmethod
    def update_my_profile(
        db: Session,
        current_employee: Employee,
        update_data: dict,
        request: Request
    ) -> dict:
        return EmployeeProfileService.update_employee_profile(
            db, current_employee.id, update_data, request
        )
