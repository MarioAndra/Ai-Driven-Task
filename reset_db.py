from sqlmodel import SQLModel
from app.core.database import engine

def reset_db():
    print("🔄 Dropping all tables...")
    SQLModel.metadata.drop_all(bind=engine)
    print("✅ All tables dropped.")

    print("🔄 Creating all tables...")
    SQLModel.metadata.create_all(bind=engine)
    print("✅ All tables created successfully.")

if __name__ == "__main__":
    reset_db()
