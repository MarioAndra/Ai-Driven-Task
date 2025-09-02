import random
from sqlmodel import Session, select
from datetime import date
from app.core.database import engine
from app.models.employee import Employee, EmployeeStatus
from app.models.skill import Skill
from app.models.EmployeeSkillLink import EmployeeSkillLink
from app.core.security import hash_password


def create_db_and_tables_if_not_exist():
    """
    Creates database tables based on the SQLModel metadata.
    """
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)


def seed_database():
    """
    Seeds the database with predefined skills and employees.
    """
    with Session(engine) as session:
        print("--- Seeding database started ---")

        # 1. Add programming and tech-related skills
        skills_to_create = [
            "Python", "JavaScript", "TypeScript", "Node.js", "React", "Vue.js",
            "Angular", "Django", "Flask", "FastAPI", "SQLAlchemy", "SQLModel",
            "HTML", "CSS", "SASS", "Tailwind CSS", "Bootstrap", "RESTful API",
            "GraphQL", "Docker", "Kubernetes", "AWS", "Azure", "Google Cloud",
            "Git", "GitHub", "GitLab", "CI/CD", "Linux", "Nginx",
            "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
            "Data Science", "Machine Learning", "Artificial Intelligence",
            "Cybersecurity", "Blockchain", "Laravel", "PHP", "Svelte",
            "Next.js", "Nuxt.js", "Express", "Spring Boot", "Ruby on Rails",
            "ASP.NET", "MariaDB", "DynamoDB", "Firebase", "SQLite",
            "GCP", "DigitalOcean", "on-prem", "Serverless", "Stripe",
            "PayPal", "payment gateway", "Payments", "PCI-DSS", "Responsive Design",
            "Mobile-first", "PWA", "Accessibility", "RTL", "WebSocket",
            "Webhooks", "D3.js", "Chart.js", "Highcharts", "Cypress",
            "Playwright", "Jest", "PHPUnit", "Terraform", "S3", "CDN",
            "Object storage", "Image optimization", "GDPR", "HIPAA",
            "OWASP", "WAF", "React Native", "Flutter", "iOS", "Android",
            "Authentication", "OAuth", "SSO", "Two-factor", "2FA",
            "Email verification"
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

        # 2. Add specific employees with requested data
        specific_employees = [
            {
                "name": "Mario Andrawos",
                "email": "marioandrawos02@gmail.com",
                "phone_number": "0937723418",
                "address": "Damascus, Syria",
                "birth_date": date(2002, 1, 20)
            },
            {
                "name": "Milad Andrawos",
                "email": "milad7076@gmail.com",
                "phone_number": "0997614102",
                "address": "Damascus, Syria",
                "birth_date": date(1996, 5, 15)
            },
            {
                "name": "Majd Alaraki",
                "email": "majd.araki2003@gmail.com",
                "phone_number": "0992686807",
                "address": "Homs, Syria",
                "birth_date": date(2003, 9, 28)
            },
            {
                "name": "Rony Mansour",
                "email": "rony@gmail.com",
                "phone_number": "0981562320",
                "address": "Damascus, Syria",
                "birth_date": date(1999, 3, 11)
            },
            {
                "name": "Rajaa Al sari",
                "email": "rajaa@gmail.com",
                "phone_number": "0945123456",
                "address": "Daraa, Syria",
                "birth_date": date(1995, 7, 5)
            }
        ]

        # 3. Add 10 additional random employees
        random_employees = [
            {
                "name": "John Smith",
                "email": "john.smith@example.com",
                "phone_number": "0932123456",
                "address": "Aleppo, Syria",
                "birth_date": date(1990, 4, 12)
            },
            {
                "name": "Emily Johnson",
                "email": "emily.j@example.com",
                "phone_number": "0994567890",
                "address": "Latakia, Syria",
                "birth_date": date(1988, 8, 25)
            },
            {
                "name": "Michael Brown",
                "email": "michael.b@example.com",
                "phone_number": "0941234567",
                "address": "Hama, Syria",
                "birth_date": date(1995, 1, 30)
            },
            {
                "name": "Jessica Davis",
                "email": "jessica.davis@example.com",
                "phone_number": "0937890123",
                "address": "Deir Ezzor, Syria",
                "birth_date": date(1992, 6, 18)
            },
            {
                "name": "Daniel Miller",
                "email": "daniel.m@example.com",
                "phone_number": "0999012345",
                "address": "Tartus, Syria",
                "birth_date": date(1985, 11, 7)
            },
            {
                "name": "Sarah Wilson",
                "email": "sarah.w@example.com",
                "phone_number": "0946789012",
                "address": "Al-Hasakah, Syria",
                "birth_date": date(1998, 2, 9)
            },
            {
                "name": "David Moore",
                "email": "david.moore@example.com",
                "phone_number": "0991234567",
                "address": "Ar-Raqqah, Syria",
                "birth_date": date(1993, 7, 21)
            },
            {
                "name": "Jennifer Taylor",
                "email": "jennifer.t@example.com",
                "phone_number": "0934567890",
                "address": "As-Suwayda, Syria",
                "birth_date": date(1997, 10, 5)
            },
            {
                "name": "Robert Clark",
                "email": "robert.c@example.com",
                "phone_number": "0998765432",
                "address": "Quneitra, Syria",
                "birth_date": date(1989, 3, 2)
            },
            {
                "name": "Linda White",
                "email": "linda.w@example.com",
                "phone_number": "0943210987",
                "address": "Idlib, Syria",
                "birth_date": date(1994, 9, 14)
            }
        ]

        # Combine all employees into a single list
        all_employees_data = specific_employees + random_employees

        # 4. Add all employees to the database
        all_employees = []
        for emp_data in all_employees_data:
            statement = select(Employee).where(Employee.email == emp_data["email"])
            if not session.exec(statement).first():
                new_employee = Employee(
                    name=emp_data["name"],
                    email=emp_data["email"],
                    password=hash_password("password"),
                    task_capacity=8,
                    available_hours=8,
                    phone_number=emp_data["phone_number"],
                    address=emp_data["address"],
                    birth_date=emp_data["birth_date"],
                    status=EmployeeStatus.available  # Set all to available
                )
                session.add(new_employee)
                all_employees.append(new_employee)
                print(f"Created employee: {new_employee.name}")
        session.commit()
        for emp in all_employees:
            session.refresh(emp)

        # 5. Link employees to skills
        for employee in all_employees:
            num_skills_to_add = random.randint(3, 7)
            selected_skills = random.sample(list(skills_in_db.values()), num_skills_to_add)

            for skill_obj in selected_skills:
                link = EmployeeSkillLink(
                    employee_id=employee.id,
                    skill_id=skill_obj.id,
                    rating=random.randint(1, 5)
                )
                session.add(link)
                print(f"  -> Linked '{employee.name}' with skill '{skill_obj.name}' with rating {link.rating}")

        session.commit()
        print("--- ✅ Seeding database finished successfully ---")


if __name__ == "__main__":
    create_db_and_tables_if_not_exist()
    seed_database()