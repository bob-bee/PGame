# backend/database.py
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlmodel import SQLModel

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://p_user:p_password@db:5432/p_threads"
)

# Convert sync postgresql driver URL to asyncpg if needed
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# echo=True logs generated SQL to the console
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def init_db() -> None:
    """Create all tables defined in our models asynchronously."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    """FastAPI Dependency for database sessions (Async)."""
    async with async_session() as session:
        yield session

async def get_db():
    """FastAPI Dependency for database sessions (Async) alias."""
    async with async_session() as session:
        yield session