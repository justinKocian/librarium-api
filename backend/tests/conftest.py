import os
from pathlib import Path
from dotenv import load_dotenv
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# Load environment
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# ENUMs aren't dropped when all tables are dropped
def drop_enum_types(engine):
    with engine.connect() as conn:
        conn.execute(text("DROP TYPE IF EXISTS readstatus CASCADE"))
        conn.commit()

# Reset DB schema once for all tests
@pytest.fixture(scope="session", autouse=True)
def reset_database():
    drop_enum_types(engine)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

# FastAPI test client
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
