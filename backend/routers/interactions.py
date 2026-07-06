# backend/routers/interactions.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_session
from models import Statement, CommunityResponse, Reaction, User
from schemas import ResponseCreate, ReactionCreate
from dependencies import get_current_user

router = APIRouter(tags=["Community Interactions"])

@router.post("/responses", response_model=CommunityResponse, status_code=status.HTTP_201_CREATED)
def post_community_response(
    response_data: ResponseCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Allows standard citizens to post structured feedback on official statement targets."""
    statement = session.get(Statement, response_data.statement_id)
    if not statement:
        raise HTTPException(status_code=404, detail="Target official statement not found")

    new_response = CommunityResponse(
        type=response_data.type,
        body=response_data.body,
        statement_id=response_data.statement_id,
        user_id=current_user.id
    )
    session.add(new_response)
    session.commit()
    session.refresh(new_response)
    return new_response

@router.post("/reactions", status_code=status.HTTP_200_OK)
def toggle_statement_reaction(
    reaction_data: ReactionCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Saves user vote metrics. Toggles or replaces existing selections."""
    statement = session.get(Statement, reaction_data.statement_id)
    if not statement:
        raise HTTPException(status_code=404, detail="Target statement not found")

    # Check if user already registered a reaction on this statement
    existing_reaction = session.exec(
        select(Reaction).where(
            Reaction.statement_id == reaction_data.statement_id,
            Reaction.user_id == current_user.id
        )
    ).first()

    if existing_reaction:
        if existing_reaction.reaction == reaction_data.reaction:
            # If clicked identical option twice, retract the vote entirely
            session.delete(existing_reaction)
            session.commit()
            return {"message": "Reaction removed"}
        else:
            # Mutate reaction variant type
            existing_reaction.reaction = reaction_data.reaction
            session.add(existing_reaction)
            session.commit()
            return {"message": "Reaction updated"}
            
    # Pure fresh insert
    new_reaction = Reaction(
        reaction=reaction_data.reaction,
        statement_id=reaction_data.statement_id,
        user_id=current_user.id
    )
    session.add(new_reaction)
    session.commit()
    return {"message": "Reaction recorded"}