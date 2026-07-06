# backend/schemas.py
from pydantic import BaseModel, EmailStr
from models import UserRole, ResponseType

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class ThreadCreate(BaseModel):
    title: str
    category: str

class StatementCreate(BaseModel):
    thread_id: int
    body: str

class ResponseCreate(BaseModel):
    statement_id: int
    type: ResponseType
    body: str

class ReactionCreate(BaseModel):
    statement_id: int
    reaction: str