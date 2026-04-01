from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.models.board import Board
from app.models.list import List
from app.models.card import Card


async def create_board(db: AsyncSession, data):
    board = Board(**data.model_dump())

    db.add(board)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Board title already exists")
    await db.refresh(board)

    return board


async def get_boards(db: AsyncSession):
    result = await db.execute(
        select(Board)
        .options(
            selectinload(Board.lists)
            .selectinload(List.cards)
        )
        .order_by(Board.created_at.desc())
    )

    return result.scalars().all()


async def get_board(db: AsyncSession, board_id: int):
    result = await db.execute(
        select(Board)
        .options(
            selectinload(Board.lists)
            .selectinload(List.cards)
        )
        .where(Board.id == board_id)
    )
    return result.scalar_one_or_none()
    