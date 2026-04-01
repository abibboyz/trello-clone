from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.list import List
from app.models.board import Board
from app.models.card import Card


async def create_list(db: AsyncSession, data):
    board_exists = await db.scalar(select(Board.id).where(Board.id == data.board_id))
    if board_exists is None:
        raise HTTPException(status_code=404, detail=f"Board {data.board_id} not found")

    lst = List(**data.model_dump())
    db.add(lst)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Invalid list data")
    await db.refresh(lst)
    return lst


async def get_lists(db: AsyncSession):
    result = await db.execute(
        select(List)
        .options(selectinload(List.cards))
        .order_by(List.created_at.desc())
    )
    return result.scalars().all()


async def get_list(db: AsyncSession, list_id: int):
    result = await db.execute(
        select(List)
        .options(selectinload(List.cards))
        .where(List.id == list_id)
    )
    return result.scalar_one_or_none()