from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Boolean, DateTime, func
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.list import List


class Board(Base):
    """Trello Board model - represents a project board"""
    __tablename__ = "boards"

    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # Columns with type hints
    title: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True, default=None)
    
    # Timestamps with server defaults
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        server_default=func.now(), 
        onupdate=func.now()
    )
    
    # Boolean with default
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships with type hints
    lists: Mapped[list["List"]] = relationship(
        back_populates="board",
        cascade="all, delete-orphan",
        lazy="selectin"  # Eager load by default
    )

    def __repr__(self) -> str:
        return f"<Board(id={self.id}, title={self.title})>"
