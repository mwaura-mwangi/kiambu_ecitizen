from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Database connection URL (use SQLite for dev, Postgres for prod)
# Postgres: "postgresql://user:pass@localhost/ecitizen"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ecitizen.db")

# Create database engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Create session maker
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    """
    Yield a database session and close it when done.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
