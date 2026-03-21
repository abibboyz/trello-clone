from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

class CardBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    position: int = 0
    is_completed: bool = False

class CardCreate(CardBase):
    list_id: int

class Card(CardBase):
    id: int
    list_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
