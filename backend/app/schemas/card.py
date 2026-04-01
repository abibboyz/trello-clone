from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class CardBase(BaseModel):
    title: str
    description: Optional[str] = None


class CardCreate(CardBase):
    list_id: int


class CardResponse(CardBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    list_id: int
    created_at: datetime
    updated_at: datetime
