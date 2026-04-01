from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.card import Card
from app.models.list import List


async def create_card(db: AsyncSession, data):
    list_exists = await db.scalar(select(List.id).where(List.id == data.list_id))
    if list_exists is None:
        raise HTTPException(status_code=404, detail=f"List {data.list_id} not found")

    card = Card(**data.model_dump())
    db.add(card)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Invalid card data")
    await db.refresh(card)
    return card


async def get_cards(db: AsyncSession):
    result = await db.execute(
        select(Card)
        .order_by(Card.created_at.desc())
    )
    return result.scalars().all()


async def get_card(db: AsyncSession, card_id: int):
    result = await db.execute(
        select(Card)
        .where(Card.id == card_id)
    )
    return result.scalar_one_or_none()