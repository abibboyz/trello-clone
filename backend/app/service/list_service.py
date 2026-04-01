from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.list import List


async def create_list(db: AsyncSession, data):
    lst = List(**data.model_dump())
    db.add(lst)
    await db.commit()
    await db.refresh(lst)
    return lst