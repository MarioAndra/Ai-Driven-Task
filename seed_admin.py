from sqlmodel import Session, select
from app.models.Admin import Admin
from app.core.security import hash_password
from app.core.config import settings
from sqlalchemy import create_engine


engine = create_engine(settings.DATABASE_URL)


def create_admin_user():
    admin_name = "admin"
    admin_email = "admin@example.com"
    admin_password = "adminadmin"

    with Session(engine) as session:

        existing_admin = session.exec(
            select(Admin).where(Admin.email == admin_email)
        ).first()

        if existing_admin:
            print("✅ Admin user already exists.")
            return


        new_admin = Admin(
            name=admin_name,
            email=admin_email,
            password=hash_password(admin_password),
            role="admin"
        )

        session.add(new_admin)
        session.commit()
        session.refresh(new_admin)

        print(f"✅ Admin user created: {new_admin.email}")


if __name__ == "__main__":
    create_admin_user()
