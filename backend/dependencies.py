# backend/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_session
from models import User, UserRole
from security import SECRET_KEY, ALGORITHM
from typing import AsyncGenerator

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

class MockRedis:
    """Placeholder Redis client for future caching implementation."""
    async def get(self, key: str) -> str | None:
        return None

    async def set(self, key: str, value: str, ex: int | None = None) -> None:
        pass

    async def delete(self, key: str) -> None:
        pass

async def get_redis() -> AsyncGenerator[MockRedis, None]:
    """FastAPI Dependency for Redis cache client."""
    client = MockRedis()
    try:
        yield client
    finally:
        pass

async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    session: AsyncSession = Depends(get_session)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user

def require_role(allowed_roles: list[UserRole]):
    """Enforces specific user tiers (e.g., Contender or Admin only)."""
    def dependency(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Action restricted to specific user roles."
            )
        return current_user
    return dependency