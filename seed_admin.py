import random
from sqlmodel import Session, select
from faker import Faker  # مكتبة لإنشاء بيانات وهمية

# --- استيراد الموديلات وإعدادات قاعدة البيانات ---
# تأكد من أن هذه المسارات صحيحة بالنسبة لمشروعك
from app.core.database import engine
from app.models.employee import Employee
from app.models.skill import Skill
from app.models.EmployeeSkillLink import EmployeeSkillLink
# --- تعديل هنا: استيراد الدالة الصحيحة من ملف الأمان الخاص بك ---
from app.core.security import hash_password

# تهيئة Faker لإنشاء بيانات عربية
fake = Faker('ar_SA')


def create_db_and_tables_if_not_exist():
    """
    ينشئ الجداول إذا لم تكن موجودة بالفعل.
    """
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)


def seed_database():
    """
    الدالة الرئيسية لملء قاعدة البيانات بالبيانات الوهمية.
    """
    with Session(engine) as session:
        print("---  seeding database started ---")

        # --- 1. إنشاء المهارات ---
        skills_to_create = [
            "Laravel", "Vue.js", "React", "Node.js", "Python", "Django",
            "MySQL", "PostgreSQL", "MongoDB", "Docker", "AWS", "CI/CD",
            "JavaScript", "TypeScript", "PHP", "HTML", "CSS"
        ]

        skills_in_db = {}
        for skill_name in skills_to_create:
            statement = select(Skill).where(Skill.name == skill_name)
            existing_skill = session.exec(statement).first()
            if not existing_skill:
                new_skill = Skill(name=skill_name)
                session.add(new_skill)
                print(f"Created skill: {skill_name}")
                skills_in_db[skill_name] = new_skill
            else:
                skills_in_db[skill_name] = existing_skill

        session.commit()
        for skill in skills_in_db.values():
            session.refresh(skill)

        # --- 2. إنشاء الموظفين وربط المهارات ---
        num_employees = 10
        for _ in range(num_employees):
            employee_name = fake.name()
            employee_email = fake.unique.email()

            statement = select(Employee).where(Employee.email == employee_email)
            if session.exec(statement).first():
                continue

            new_employee = Employee(
                name=employee_name,
                email=employee_email,
                # --- تعديل هنا: استخدام دالة التشفير الصحيحة ---
                password=hash_password("password"),  # كلمة سر افتراضية
                task_capacity=random.randint(2, 5),
                available_hours=random.choice([4, 6, 8])
            )
            session.add(new_employee)
            session.commit()
            session.refresh(new_employee)
            print(f"Created employee: {employee_name}")

            # --- 3. ربط المهارات بشكل عشوائي ---
            num_skills_to_add = random.randint(2, 5)
            selected_skills = random.sample(list(skills_in_db.values()), num_skills_to_add)

            for skill_obj in selected_skills:
                link = EmployeeSkillLink(
                    employee_id=new_employee.id,
                    skill_id=skill_obj.id,
                    rating=random.randint(1, 5)  # تقييم عشوائي
                )
                session.add(link)
                print(f"  -> Linked skill '{skill_obj.name}' with rating {link.rating}")

        session.commit()
        print("--- ✅ Seeding database finished successfully ---")


if __name__ == "__main__":
    create_db_and_tables_if_not_exist()
    seed_database()
