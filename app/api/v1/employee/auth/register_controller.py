import os
from sqlmodel import Session
from fastapi import Request
from app.services.auth_service import register_employee, generate_token

UPLOAD_DIR = "Media/employee"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def register_controller(session: Session, request_data: dict, request: Request):
    profile_image = request_data.pop("profile_image", None)

    image_path = None
    profile_url = None

    if profile_image:
        file_ext = os.path.splitext(profile_image.filename)[1]
        file_name = f"{request_data['email']}{file_ext}"
        image_path = os.path.join(UPLOAD_DIR, file_name)

        with open(image_path, "wb") as buffer:
            buffer.write(profile_image.file.read())


        base_url = str(request.base_url).rstrip("/")
        profile_url = f"{base_url}/media/employee/{file_name}"

    employee = register_employee(
        session,
        **request_data,
        profile_image=image_path
    )

    token = generate_token(employee)

    return {
        "message": "Employee registered successfully.",
        "employee": {
            "id": employee.id,
            "name": employee.name,
            "email": employee.email,
            "role": employee.role,
            "status": employee.status,
            "task_capacity": employee.task_capacity,
            "available_hours": employee.available_hours,
            "phone_number": employee.phone_number,
            "address": employee.address,
            "birth_date": employee.birth_date,
            "profile_image": profile_url or "",
        },
        "access_token": token,
    }
