from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.schemas.list import ListCreate, ListResponse
from app.service.list_service import create_list, get_lists, get_list

router = APIRouter(prefix="/lists", tags=["Lists"])


@router.post(
    "/",
    response_model=ListResponse,
    responses={
        400: {"description": "Invalid list data"},
        404: {"description": "Board not found"},
    },
)
async def create_list_route(data: ListCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new list for a board.
    """
    return await create_list(db, data)


@router.get("/", response_model=List[ListResponse])
async def read_all_lists(db: AsyncSession = Depends(get_db)):
    """
    Get all lists.
    (Optional: later you can filter by board_id)
    """
    return await get_lists(db)


@router.get("/{list_id}", response_model=ListResponse)
async def read_one_list(list_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a single list by ID, including its cards.
    """
    lst = await get_list(db, list_id)
    if not lst:
        raise HTTPException(status_code=404, detail="List not found")
    return lst