import os
import time
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ✅ Load .env from project root
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

# 🔧 Read DB connection URL
DATABASE_URL = os.getenv("DATABASE_URL")
print("🔍 DATABASE_URL from env:", DATABASE_URL)

# 🔁 Retry DB connection
def create_engine_with_retry(url):
    for i in range(10):
        try:
            engine = create_engine(url)
            connection = engine.connect()
            connection.close()
            print("✅ Database connected!")
            return engine
        except Exception:
            print(f"⏳ Database not ready (attempt {i+1}/10), retrying...")
            time.sleep(2)
    raise Exception("❌ Could not connect to the database after 10 attempts.")

# 🧱 SQLAlchemy setup
engine = create_engine_with_retry(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 🔄 FastAPI DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Import models only after Base is declared to avoid circular imports
from app.models import user_books
