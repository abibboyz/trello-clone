from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional

from app.schemas.list import ListResponse


class BoardBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_active: bool = True


class BoardCreate(BoardBase):
    pass


class BoardResponse(BoardBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

    lists: List[ListResponse] = []


# ✅ REQUIRED
BoardResponse.model_rebuild()