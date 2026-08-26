from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# For quick start use SQLite, later change to Postgres
# Postgres: "postgresql://user:pass@localhost/ecitizen"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ecitizen.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()