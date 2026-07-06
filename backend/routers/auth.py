# backend/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_session
from models import User, UserRole
from schemas import UserCreate
from security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    # Check for duplicate registration attributes
    result = await session.execute(select(User).where(User.username == user_data.username))
    existing_username = result.scalars().first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already registered")
        
    result = await session.execute(select(User).where(User.email == user_data.email))
    existing_email = result.scalars().first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    # Salt and hash password before database persistence
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        role=UserRole.USER  # Defaults to standard user tier
    )
    
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return {"message": "User registered successfully", "user_id": new_user.id}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.username == form_data.username))
    user = result.scalars().first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # Generate stateless session payload
    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}