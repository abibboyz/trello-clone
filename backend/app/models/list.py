from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, func
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.board import Board
    from app.models.card import Card


class List(Base):
    """Trello List model - represents a column in a board"""
    __tablename__ = "lists"

    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # Foreign Key with type hint
    board_id: Mapped[int] = mapped_column(ForeignKey("boards.id"), index=True)
    
    # Regular columns
    title: Mapped[str] = mapped_column(String(255), index=True)
    position: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    board: Mapped["Board"] = relationship(back_populates="lists", lazy="joined")
    cards: Mapped[list["Card"]] = relationship(
        back_populates="list",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<List(id={self.id}, title={self.title}, board_id={self.board_id})>"
