from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, func
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.list import List


class Card(Base):
    """Trello Card model - represents a task in a list"""
    __tablename__ = "cards"

    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # Foreign Key
    list_id: Mapped[int] = mapped_column(ForeignKey("lists.id"), index=True)
    
    # Columns
    title: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str | None] = mapped_column(String(2000), nullable=True, default=None)
    position: Mapped[int] = mapped_column(Integer, default=0)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    # Relationships
    list: Mapped["List"] = relationship(back_populates="cards", lazy="joined")

    def __repr__(self) -> str:
        return f"<Card(id={self.id}, title={self.title})>"
