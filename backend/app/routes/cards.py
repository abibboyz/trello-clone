from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.schemas.card import CardCreate, CardResponse
from app.service.card_service import create_card

router = APIRouter(prefix="/cards", tags=["Cards"])


@router.post("/", response_model=CardResponse)
async def create_card_route(data: CardCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new card.
    """
    return await create_card(db, data)


@router.get("/", response_model=List[CardResponse])
async def read_all_cards(db: AsyncSession = Depends(get_db)):
    """
    Get all cards. 
    (Optional: later you can filter by list_id or board_id)
    """
    # If you want all cards in DB
    # You would need to implement get_all_cards(db) in CRUD
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/{card_id}", response_model=CardResponse)
async def read_one_card(card_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a single card by ID.
    (Optional: implement get_card(db, card_id) in CRUD)
    """
    # You need to implement this in CRUD first
    raise HTTPException(status_code=501, detail="Not implemented yet")