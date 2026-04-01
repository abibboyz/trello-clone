from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.schemas.board import BoardCreate, BoardResponse  # use BoardResponse for responses
from app.service.board_service import create_board, get_boards, get_board

router = APIRouter(prefix="/boards", tags=["Boards"])


@router.post(
    "/",
    response_model=BoardResponse,
    responses={400: {"description": "Board title already exists"}},
)
async def create_board_route(data: BoardCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new board.
    """
    return await create_board(db, data)


@router.get("/", response_model=List[BoardResponse])
async def read_all_boards(db: AsyncSession = Depends(get_db)):
    """
    Get all boards with their lists and cards.
    """
    return await get_boards(db)


@router.get("/{board_id}", response_model=BoardResponse)
async def read_one_board(board_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a single board by ID, including its lists and cards.
    """
    board = await get_board(db, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return board