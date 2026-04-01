from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List

# 👇 import AFTER future annotations
from app.schemas.card import CardResponse


class ListBase(BaseModel):
    title: str


class ListCreate(ListBase):
    board_id: int


class ListResponse(ListBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    board_id: int
    created_at: datetime

    cards: List[CardResponse] = []


# ✅ REQUIRED in Pydantic v2 for forward refs
ListResponse.model_rebuild()