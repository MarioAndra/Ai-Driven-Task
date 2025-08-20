# seed_admin.py
from app.core.database import get_session
from app.models.Admin import Admin
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

# إعداد تشفير الباسورد
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def seed_admin(db):
    """تضيف Admin إذا مش موجود"""
    admin_email = "admin@example.com"
    admin_name = "Admin"
    admin_password = "admin"

    existing_admin = db.query(Admin).filter(Admin.email == admin_email).first()
    if existing_admin:
        print("ℹ️ Admin already exists.")
        return

    new_admin = Admin(
        name=admin_name,
        email=admin_email,
        password=get_password_hash(admin_password),
        role="admin"
    )
    db.add(new_admin)
    try:
        db.commit()
        db.refresh(new_admin)
        print("✅ Admin created successfully!")
    except IntegrityError:
        db.rollback()
        print("❌ Failed to create admin. Possibly duplicate email.")

if __name__ == "__main__":
    with next(get_session()) as db:
        seed_admin(db)
