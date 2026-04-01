from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.schemas.card import CardCreate, CardResponse
from app.service.card_service import create_card, get_cards, get_card

router = APIRouter(prefix="/cards", tags=["Cards"])


@router.post(
    "/",
    response_model=CardResponse,
    responses={
        400: {"description": "Invalid card data"},
        404: {"description": "List not found"},
    },
)
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
    return await get_cards(db)


@router.get("/{card_id}", response_model=CardResponse)
async def read_one_card(card_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a single card by ID.
    (Optional: implement get_card(db, card_id) in CRUD)
    """
    card = await get_card(db, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card