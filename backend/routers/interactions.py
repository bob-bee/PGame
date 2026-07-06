# backend/routers/interactions.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_session
from models import Statement, CommunityResponse, Reaction, User
from schemas import ResponseCreate, ReactionCreate, ResponseRead
from dependencies import get_current_user

router = APIRouter(tags=["Community Interactions"])

@router.post("/responses", response_model=ResponseRead, status_code=status.HTTP_201_CREATED)
async def post_community_response(
    response_data: ResponseCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Allows standard citizens to post structured feedback on official statement targets."""
    statement = await session.get(Statement, response_data.statement_id)
    if not statement:
        raise HTTPException(status_code=404, detail="Target official statement not found")

    new_response = CommunityResponse(
        type=response_data.type,
        body=response_data.body,
        statement_id=response_data.statement_id,
        user_id=current_user.id
    )
    session.add(new_response)
    await session.commit()
    await session.refresh(new_response)
    return new_response

@router.post("/reactions", status_code=status.HTTP_200_OK)
async def toggle_statement_reaction(
    reaction_data: ReactionCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Saves user vote metrics. Toggles or replaces existing selections."""
    statement = await session.get(Statement, reaction_data.statement_id)
    if not statement:
        raise HTTPException(status_code=404, detail="Target statement not found")

    # Check if user already registered a reaction on this statement
    result = await session.execute(
        select(Reaction).where(
            Reaction.statement_id == reaction_data.statement_id,
            Reaction.user_id == current_user.id
        )
    )
    existing_reaction = result.scalars().first()

    if existing_reaction:
        if existing_reaction.reaction == reaction_data.reaction:
            # If clicked identical option twice, retract the vote entirely
            await session.delete(existing_reaction)
            await session.commit()
            return {"message": "Reaction removed"}
        else:
            # Mutate reaction variant type
            existing_reaction.reaction = reaction_data.reaction
            session.add(existing_reaction)
            await session.commit()
            return {"message": "Reaction updated"}
            
    # Pure fresh insert
    new_reaction = Reaction(
        reaction=reaction_data.reaction,
        statement_id=reaction_data.statement_id,
        user_id=current_user.id
    )
    session.add(new_reaction)
    await session.commit()
    return {"message": "Reaction recorded"}