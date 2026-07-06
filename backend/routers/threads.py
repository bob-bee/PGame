# backend/routers/threads.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_session
from models import Thread, Statement, User, UserRole, ThreadStatus
from schemas import ThreadCreate, StatementCreate, ThreadRead, StatementRead
from dependencies import get_current_user, require_role

router = APIRouter(prefix="/threads", tags=["Threads & Statements"])

@router.post("", response_model=ThreadRead, status_code=status.HTTP_201_CREATED)
async def create_thread(
    thread_data: ThreadCreate, 
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Any authenticated user can propose a new debate thread."""
    new_thread = Thread(
        title=thread_data.title,
        category=thread_data.category,
        creator_id=current_user.id,
        status=ThreadStatus.PROPOSED  # Defaults to proposed until community ups it
    )
    session.add(new_thread)
    await session.commit()
    await session.refresh(new_thread)
    return new_thread

@router.get("", response_model=List[ThreadRead])
async def list_threads(session: AsyncSession = Depends(get_session)):
    """Public read access for all threads."""
    result = await session.execute(select(Thread))
    return result.scalars().all()

@router.get("/{thread_id}")
async def get_thread_details(thread_id: int, session: AsyncSession = Depends(get_session)):
    """Fetch a specific thread along with all official statements posted to it."""
    thread = await session.get(Thread, thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    # Eagerly pull associated statements
    result = await session.execute(select(Statement).where(Statement.thread_id == thread_id))
    statements = result.scalars().all()
    
    return {
        "thread": thread,
        "statements": statements
    }

@router.post("/{thread_id}/statements", response_model=StatementRead, status_code=status.HTTP_201_CREATED)
async def post_official_statement(
    thread_id: int,
    statement_data: StatementCreate,
    session: AsyncSession = Depends(get_session),
    # Guard: Enforces that the current authenticated user has the CONTENDER role
    current_contender: User = Depends(require_role([UserRole.CONTENDER]))
):
    """Allows verified Contenders to publish official viewpoints on a thread."""
    thread = await session.get(Thread, thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
        
    if thread.status == ThreadStatus.ARCHIVED:
        raise HTTPException(status_code=400, detail="Cannot post statements to an archived thread")

    new_statement = Statement(
        body=statement_data.body,
        thread_id=thread_id,
        contender_id=current_contender.id
    )
    
    # Optional logic: automatically lift thread to ACTIVE status when a contender engages
    if thread.status == ThreadStatus.PROPOSED:
        thread.status = ThreadStatus.ACTIVE
        session.add(thread)

    session.add(new_statement)
    await session.commit()
    await session.refresh(new_statement)
    return new_statement