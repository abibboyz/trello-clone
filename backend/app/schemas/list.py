class ListBase(BaseModel):
    title: str = Field(..., max_length=255)
    position: int = 0
    is_active: bool = True

class ListCreate(ListBase):
    board_id: int

class List(ListBase):
    id: int
    board_id: int
    created_at: datetime
    # Nested cards for the full JSON response
    cards: list[Card] = []

    model_config = ConfigDict(from_attributes=True)
