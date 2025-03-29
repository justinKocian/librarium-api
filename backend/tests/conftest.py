import os
from pathlib import Path
from dotenv import load_dotenv
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# ✅ Load .env from project root
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

# 🔧 Read DB connection URL
DATABASE_URL = os.getenv("DATABASE_URL")
print("🔧 Using DATABASE_URL:", DATABASE_URL)

# 🧱 Setup SQLAlchemy test session
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🔁 Override get_db for tests
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# 🔄 Reset DB schema before test session
@pytest.fixture(scope="session", autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

# 🚀 Provide FastAPI test client
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
