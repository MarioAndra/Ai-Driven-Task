# app/services/employee_update.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.employee import Employee
from app.schemas.employee import EmployeeUpdateRequest
from app.services.employee_profile import EmployeeProfileService # استيراد الخدمة الأخرى

class EmployeeUpdateService:
    @staticmethod
    def update_employee_profile(db: Session, employee_id: int, update_data: EmployeeUpdateRequest):
        
        employee = db.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found."
            )
        
        # تحديث الحقول فقط إذا تم توفيرها في الطلب
        # في Pydantic v2، يفضل استخدام model_dump(exclude_unset=True)
        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(employee, key, value)

        db.add(employee)
        db.commit()
        db.refresh(employee)
        
        # بعد التحديث، قم باستدعاء خدمة جلب الملف الشخصي
        # لضمان إرجاع كائن EmployeeProfile كاملاً مع المهارات
        return EmployeeProfileService.get_employee_profile(db, employee.id)
