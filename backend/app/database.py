import os
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

# Retry logic to wait for DB container to be ready
for i in range(10):
    try:
        engine = create_engine(DATABASE_URL)
        connection = engine.connect()
        connection.close()
        print("✅ Database connected!")
        break
    except Exception as e:
        print(f"⏳ Database not ready (attempt {i+1}/10), retrying...")
        time.sleep(2)
else:
    raise Exception("❌ Could not connect to the database after 10 attempts.")

# SQLAlchemy session setup
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to inject DB session into routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
