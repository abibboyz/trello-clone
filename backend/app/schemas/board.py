class BoardBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    is_active: bool = True

class BoardCreate(BoardBase):
    pass

class Board(BoardBase):
    id: int
    created_at: datetime
    updated_at: datetime
    # Nested lists which include nested cards
    lists: list[List] = []

    model_config = ConfigDict(from_attributes=True)
