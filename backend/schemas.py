# backend/schemas.py
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict
from models import UserRole, ResponseType, ThreadStatus

# --- USER SCHEMAS ---
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# --- THREAD SCHEMAS ---
class ThreadCreate(BaseModel):
    title: str
    category: str

class ThreadRead(BaseModel):
    id: int
    title: str
    category: str
    status: ThreadStatus
    created_at: datetime
    creator_id: int

    model_config = ConfigDict(from_attributes=True)

# --- STATEMENT SCHEMAS ---
class StatementCreate(BaseModel):
    thread_id: int
    body: str

class StatementRead(BaseModel):
    id: int
    body: str
    created_at: datetime
    thread_id: int
    contender_id: int

    model_config = ConfigDict(from_attributes=True)

# --- RESPONSE SCHEMAS ---
class ResponseCreate(BaseModel):
    statement_id: int
    type: ResponseType
    body: str

class ResponseRead(BaseModel):
    id: int
    type: ResponseType
    body: str
    created_at: datetime
    statement_id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)

# --- REACTION SCHEMAS ---
class ReactionCreate(BaseModel):
    statement_id: int
    reaction: str

class ReactionRead(BaseModel):
    id: int
    reaction: str
    created_at: datetime
    statement_id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)