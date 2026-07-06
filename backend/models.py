# backend/models.py
from datetime import datetime
from enum import Enum
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

class UserRole(str, Enum):
    USER = "user"
    CONTENDER = "contender"
    ADMIN = "admin"

class ResponseType(str, Enum):
    EVIDENCE = "evidence"
    QUESTION = "question"
    COUNTER_ARGUMENT = "counterargument"

class ThreadStatus(str, Enum):
    PROPOSED = "proposed"
    ACTIVE = "active"
    ARCHIVED = "archived"

# --- USER MODEL ---
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False)
    email: str = Field(unique=True, nullable=False)
    password_hash: str = Field(nullable=False)
    role: UserRole = Field(default=UserRole.USER)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships (Using selectin loading for async capability)
    threads: List["Thread"] = Relationship(
        back_populates="creator",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    statements: List["Statement"] = Relationship(
        back_populates="contender",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    responses: List["CommunityResponse"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    reactions: List["Reaction"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

# --- THREAD MODEL ---
class Thread(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    category: str = Field(index=True, nullable=False)
    status: ThreadStatus = Field(default=ThreadStatus.PROPOSED)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    creator_id: int = Field(foreign_key="user.id", nullable=False, index=True)
    creator: User = Relationship(
        back_populates="threads",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    
    statements: List["Statement"] = Relationship(
        back_populates="thread",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

# --- STATEMENT MODEL (Contenders Only) ---
class Statement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    body: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    thread_id: int = Field(foreign_key="thread.id", nullable=False, index=True)
    thread: Thread = Relationship(
        back_populates="statements",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    contender_id: int = Field(foreign_key="user.id", nullable=False, index=True)
    contender: User = Relationship(
        back_populates="statements",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    responses: List["CommunityResponse"] = Relationship(
        back_populates="statement",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    reactions: List["Reaction"] = Relationship(
        back_populates="statement",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

# --- COMMUNITY RESPONSE MODEL ---
class CommunityResponse(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: ResponseType = Field(nullable=False)
    body: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    statement_id: int = Field(foreign_key="statement.id", nullable=False, index=True)
    statement: Statement = Relationship(
        back_populates="responses",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    user_id: int = Field(foreign_key="user.id", nullable=False, index=True)
    user: User = Relationship(
        back_populates="responses",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

# --- REACTION MODEL ---
class Reaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    reaction: str = Field(nullable=False) # e.g., "agree", "disagree", "neutral"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    statement_id: int = Field(foreign_key="statement.id", nullable=False, index=True)
    statement: Statement = Relationship(
        back_populates="reactions",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    user_id: int = Field(foreign_key="user.id", nullable=False, index=True)
    user: User = Relationship(
        back_populates="reactions",
        sa_relationship_kwargs={"lazy": "selectin"}
    )