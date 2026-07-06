# backend/database.py
import os
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://p_user:p_password@db:5432/p_threads"
)

# echo=True logs generated SQL to the console, which is helpful during rapid dev
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    """Create all tables defined in our models."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """FastAPI Dependency for database sessions."""
    with Session(engine) as session:
        yield session