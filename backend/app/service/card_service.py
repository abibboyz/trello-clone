from sqlalchemy.ext.asyncio import AsyncSession
from app.models.card import Card


async def create_card(db: AsyncSession, data):
    card = Card(**data.model_dump())
    db.add(card)
    await db.commit()
    await db.refresh(card)
    return card