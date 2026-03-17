# Database CRUD Guide

This guide explains how to use the database configuration for Create, Read, Update, and Delete (CRUD) operations in the Trello Clone application using **modern SQLAlchemy 2.0+ patterns**.

## Table of Contents

1. [Database Setup](#database-setup)
2. [Creating Models (Modern Way)](#creating-models-modern-way)
3. [CRUD Operations](#crud-operations)
4. [Using in FastAPI Routes](#using-in-fastapi-routes)
5. [Examples](#examples)

---

## Database Setup

The database is configured in `app/core/database.py`:

- **Engine**: Async SQLAlchemy engine for PostgreSQL
- **Session**: `AsyncSessionLocal` for database sessions
- **Base Class**: `Base` for all ORM models (using `DeclarativeBase`)
- **Dependency**: `get_db()` for FastAPI dependency injection

```python
from app.core.database import engine, AsyncSessionLocal, Base, get_db, create_tables
```

---

## Creating Models (Modern Way)

Define your database models using **modern SQLAlchemy 2.0+ patterns** with type annotations and `mapped_column`.

### Example: Board Model

Create `app/models/board.py`:

```python
from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Boolean, DateTime, func
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.list import List


class Board(Base):
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
```

### Example: List Model

Create `app/models/list.py`:

```python
from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, func
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.board import Board
    from app.models.card import Card


class List(Base):
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
```

### Example: Card Model

Create `app/models/card.py`:

```python
from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, func
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.list import List


class Card(Base):
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
```

---

## CRUD Operations

### CREATE - Add New Records

```python
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.board import Board

async def create_board(title: str, description: str | None = None) -> Board:
    """Create a new board"""
    async with AsyncSessionLocal() as session:
        # Create instance with type hints
        new_board: Board = Board(
            title=title,
            description=description
        )
        
        # Add to session
        session.add(new_board)
        
        # Commit transaction
        await session.commit()
        
        # Refresh to get ID and timestamps
        await session.refresh(new_board)
        
        return new_board
```

### READ - Fetch Records

**Get All Records:**
```python
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.board import Board

async def get_all_boards() -> list[Board]:
    """Get all active boards"""
    async with AsyncSessionLocal() as session:
        stmt = select(Board).where(Board.is_active == True)
        result = await session.execute(stmt)
        boards: list[Board] = result.scalars().all()
        return boards
```

**Get Single Record by ID:**
```python
async def get_board_by_id(board_id: int) -> Board | None:
    """Get board by ID with relationships"""
    async with AsyncSessionLocal() as session:
        stmt = select(Board).where(Board.id == board_id)
        result = await session.execute(stmt)
        board: Board | None = result.scalars().first()
        return board
```

**Get with Filtering:**
```python
async def get_boards_by_title(title: str) -> list[Board]:
    """Search boards by title"""
    async with AsyncSessionLocal() as session:
        stmt = select(Board).where(
            Board.title.ilike(f"%{title}%"),
            Board.is_active == True
        )
        result = await session.execute(stmt)
        boards: list[Board] = result.scalars().all()
        return boards
```

**Eager Load Relationships:**
```python
from sqlalchemy.orm import selectinload

async def get_board_with_lists(board_id: int) -> Board | None:
    """Get board with all lists eager loaded"""
    async with AsyncSessionLocal() as session:
        stmt = select(Board).where(Board.id == board_id).options(
            selectinload(Board.lists)
        )
        result = await session.execute(stmt)
        board: Board | None = result.scalars().first()
        return board
```

### UPDATE - Modify Records

```python
from sqlalchemy import update

async def update_board(board_id: int, title: str, description: str | None) -> Board | None:
    """Update board fields"""
    async with AsyncSessionLocal() as session:
        # Fetch the board
        stmt = select(Board).where(Board.id == board_id)
        result = await session.execute(stmt)
        board: Board | None = result.scalars().first()
        
        if not board:
            return None
        
        # Update fields
        board.title = title
        board.description = description
        
        # Commit changes
        await session.commit()
        await session.refresh(board)
        
        return board
```

**Bulk Update:**
```python
async def deactivate_board(board_id: int) -> bool:
    """Bulk update using update()"""
    async with AsyncSessionLocal() as session:
        stmt = update(Board).where(
            Board.id == board_id
        ).values(is_active=False)
        
        result = await session.execute(stmt)
        await session.commit()
        
        return result.rowcount > 0
```

### DELETE - Remove Records

**Soft Delete (Mark as Inactive):**
```python
async def delete_board_soft(board_id: int) -> bool:
    """Soft delete - mark as inactive"""
    async with AsyncSessionLocal() as session:
        stmt = select(Board).where(Board.id == board_id)
        result = await session.execute(stmt)
        board: Board | None = result.scalars().first()
        
        if not board:
            return False
        
        board.is_active = False
        await session.commit()
        
        return True
```

**Hard Delete (Permanent):**
```python
async def delete_board_hard(board_id: int) -> bool:
    """Hard delete - permanently remove"""
    async with AsyncSessionLocal() as session:
        stmt = select(Board).where(Board.id == board_id)
        result = await session.execute(stmt)
        board: Board | None = result.scalars().first()
        
        if not board:
            return False
        
        await session.delete(board)
        await session.commit()
        
        return True
```

---

## Using in FastAPI Routes

### Import Dependencies

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.board import Board
```

### Create Route with DB Dependency

```python
router = APIRouter(prefix="/boards", tags=["boards"])


@router.post("/", response_model=dict)
async def create_board(
    title: str,
    description: str | None = None,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """Create a new board"""
    new_board: Board = Board(title=title, description=description)
    db.add(new_board)
    await db.commit()
    await db.refresh(new_board)
    return {"id": new_board.id, "title": new_board.title}


@router.get("/{board_id}", response_model=dict)
async def get_board(
    board_id: int,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """Get board by ID"""
    stmt = select(Board).where(Board.id == board_id)
    result = await db.execute(stmt)
    board: Board | None = result.scalars().first()
    
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    
    return {
        "id": board.id,
        "title": board.title,
        "description": board.description,
        "lists_count": len(board.lists)
    }


@router.put("/{board_id}", response_model=dict)
async def update_board(
    board_id: int,
    title: str,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """Update board"""
    stmt = select(Board).where(Board.id == board_id)
    result = await db.execute(stmt)
    board: Board | None = result.scalars().first()
    
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    
    board.title = title
    await db.commit()
    await db.refresh(board)
    return {"id": board.id, "title": board.title}


@router.delete("/{board_id}")
async def delete_board(
    board_id: int,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """Delete board"""
    stmt = select(Board).where(Board.id == board_id)
    result = await db.execute(stmt)
    board: Board | None = result.scalars().first()
    
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    
    await db.delete(board)
    await db.commit()
    return {"message": "Board deleted"}
```

---

## Examples

### Complete CRUD Service

Create `app/services/board_service.py`:

```python
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.board import Board


class BoardService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, title: str, description: str | None = None) -> Board:
        """Create a new board with type hints"""
        board: Board = Board(title=title, description=description)
        self.db.add(board)
        await self.db.commit()
        await self.db.refresh(board)
        return board

    async def get_all(self) -> list[Board]:
        """Get all active boards"""
        stmt = select(Board).where(Board.is_active == True)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, board_id: int) -> Board | None:
        """Get board by ID"""
        stmt = select(Board).where(Board.id == board_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_with_lists(self, board_id: int) -> Board | None:
        """Get board with eager-loaded lists"""
        stmt = select(Board).where(Board.id == board_id)
        result = await self.db.execute(stmt)
        board: Board | None = result.scalars().first()
        # Lists are already loaded via lazy="selectin"
        return board

    async def update(self, board_id: int, **kwargs) -> Board | None:
        """Update board fields with type safety"""
        board: Board | None = await self.get_by_id(board_id)
        if not board:
            return None
        
        # Only update allowed fields
        allowed_fields = {"title", "description", "is_active"}
        for key, value in kwargs.items():
            if key in allowed_fields and hasattr(board, key):
                setattr(board, key, value)
        
        await self.db.commit()
        await self.db.refresh(board)
        return board

    async def delete(self, board_id: int, hard: bool = False) -> bool:
        """Delete board (soft or hard)"""
        board: Board | None = await self.get_by_id(board_id)
        if not board:
            return False
        
        if hard:
            await self.db.delete(board)
        else:
            board.is_active = False
        
        await self.db.commit()
        return True
```

### Use Service in Routes

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.board_service import BoardService


router = APIRouter(prefix="/boards", tags=["boards"])


@router.post("/")
async def create_board(
    title: str,
    description: str | None = None,
    db: AsyncSession = Depends(get_db)
) -> dict:
    service = BoardService(db)
    board = await service.create(title, description)
    return {"id": board.id, "title": board.title}


@router.get("/")
async def list_boards(db: AsyncSession = Depends(get_db)) -> list[dict]:
    service = BoardService(db)
    boards = await service.get_all()
    return [{"id": b.id, "title": b.title} for b in boards]


@router.get("/{board_id}")
async def get_board(
    board_id: int,
    db: AsyncSession = Depends(get_db)
) -> dict:
    service = BoardService(db)
    board = await service.get_with_lists(board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return {
        "id": board.id,
        "title": board.title,
        "description": board.description,
        "lists": [{"id": l.id, "title": l.title} for l in board.lists]
    }


@router.put("/{board_id}")
async def update_board(
    board_id: int,
    title: str | None = None,
    description: str | None = None,
    db: AsyncSession = Depends(get_db)
) -> dict:
    service = BoardService(db)
    updates = {k: v for k, v in {"title": title, "description": description}.items() if v is not None}
    board = await service.update(board_id, **updates)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return {"id": board.id, "title": board.title}


@router.delete("/{board_id}")
async def delete_board(
    board_id: int,
    hard: bool = False,
    db: AsyncSession = Depends(get_db)
) -> dict:
    service = BoardService(db)
    if not await service.delete(board_id, hard=hard):
        raise HTTPException(status_code=404, detail="Board not found")
    return {"message": "Board deleted" + (" permanently" if hard else "")}
```

---

## Initializing Tables

Run this once to create all tables:

```bash
python -c "from app.core.database import create_tables; import asyncio; asyncio.run(create_tables())"
```

Or in your main application startup:

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    await create_tables()
    print("✅ Database tables created")
    yield
    # Shutdown code here if needed
    print("🛑 Application shutdown")


app = FastAPI(lifespan=lifespan)
```

---

## Modern SQLAlchemy 2.0+ Features Used

✅ **`Mapped` Type Hints** - Full type safety with `Mapped[str]`, `Mapped[int | None]`  
✅ **`mapped_column`** - Modern column definition replacing `Column()`  
✅ **Server-side Defaults** - `server_default=func.now()` instead of Python defaults  
✅ **Type Annotations** - Complete type hints for IDE and static analysis  
✅ **`select()` Syntax** - Modern SQL expression over legacy `.query()`  
✅ **Lazy Loading** - `lazy="selectin"` for eager loading relationships  
✅ **Union Types** - `str | None` instead of `Optional[str]`  
✅ **`TYPE_CHECKING`** - Circular import prevention with forward references

---

## Best Practices

1. **Always use type hints** for columns and relationships
2. **Use `server_default`** for timestamps instead of Python defaults
3. **Use `select()` expressions** instead of `.query()`
4. **Configure lazy loading** appropriately (`selectin`, `joined`, `select`)
5. **Use `Depends(get_db)`** in FastAPI routes
6. **Refresh objects after commit** to get updated data
7. **Implement soft deletes** with `is_active` flag
8. **Use services** to centralize database logic
9. **Handle exceptions** appropriately in routes
10. **Use `mapped_column`** for all new column definitions

---

For more information, see [SQLAlchemy 2.0 Migration Guide](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html)


---

## Database Setup

The database is configured in `app/core/database.py`:

- **Engine**: Async SQLAlchemy engine for PostgreSQL
- **Session**: `AsyncSessionLocal` for database sessions
- **Base Class**: `Base` for all ORM models
- **Dependency**: `get_db()` for FastAPI dependency injection

```python
from app.core.database import engine, AsyncSessionLocal, Base, get_db, create_tables
```

---

## Creating Models

Define your database models by extending `Base` from `app/core/database.py`.

### Example: Board Model

Create `app/models/board.py`:

```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), unique=True, index=True)
    description = Column(String(1000), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationships
    lists = relationship("List", back_populates="board", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Board(id={self.id}, title={self.title})>"
```

### Example: List Model

Create `app/models/list.py`:

```python
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class List(Base):
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True, index=True)
    board_id = Column(Integer, ForeignKey("boards.id"), index=True)
    title = Column(String(255), index=True)
    position = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    board = relationship("Board", back_populates="lists")
    cards = relationship("Card", back_populates="list", cascade="all, delete-orphan")
```

---

## CRUD Operations

### CREATE - Add New Records

```python
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.board import Board

async def create_board(title: str, description: str):
    async with AsyncSessionLocal() as session:
        # Create new board instance
        new_board = Board(title=title, description=description)
        
        # Add to session
        session.add(new_board)
        
        # Commit transaction
        await session.commit()
        
        # Refresh to get the ID
        await session.refresh(new_board)
        
        return new_board
```

### READ - Fetch Records

**Get All Records:**
```python
async def get_all_boards():
    async with AsyncSessionLocal() as session:
        query = select(Board).where(Board.is_active == True)
        result = await session.execute(query)
        boards = result.scalars().all()
        return boards
```

**Get Single Record by ID:**
```python
async def get_board_by_id(board_id: int):
    async with AsyncSessionLocal() as session:
        query = select(Board).where(Board.id == board_id)
        result = await session.execute(query)
        board = result.scalars().first()
        return board
```

**Get with Filtering:**
```python
async def get_boards_by_title(title: str):
    async with AsyncSessionLocal() as session:
        query = select(Board).where(Board.title.ilike(f"%{title}%"))
        result = await session.execute(query)
        boards = result.scalars().all()
        return boards
```

### UPDATE - Modify Records

```python
async def update_board(board_id: int, title: str, description: str):
    async with AsyncSessionLocal() as session:
        # Fetch the board
        query = select(Board).where(Board.id == board_id)
        result = await session.execute(query)
        board = result.scalars().first()
        
        if not board:
            return None
        
        # Update fields
        board.title = title
        board.description = description
        
        # Commit changes
        await session.commit()
        await session.refresh(board)
        
        return board
```

### DELETE - Remove Records

**Soft Delete (Mark as Inactive):**
```python
async def delete_board_soft(board_id: int):
    async with AsyncSessionLocal() as session:
        query = select(Board).where(Board.id == board_id)
        result = await session.execute(query)
        board = result.scalars().first()
        
        if not board:
            return None
        
        board.is_active = False
        await session.commit()
        
        return {"message": "Board deleted (soft)"}
```

**Hard Delete (Permanent):**
```python
async def delete_board_hard(board_id: int):
    async with AsyncSessionLocal() as session:
        query = select(Board).where(Board.id == board_id)
        result = await session.execute(query)
        board = result.scalars().first()
        
        if not board:
            return None
        
        await session.delete(board)
        await session.commit()
        
        return {"message": "Board permanently deleted"}
```

---

## Using in FastAPI Routes

### Import Dependencies

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.board import Board
```

### Create Route with DB Dependency

```python
router = APIRouter(prefix="/boards", tags=["boards"])


@router.post("/")
async def create_board(title: str, description: str, db: AsyncSession = Depends(get_db)):
    """Create a new board"""
    new_board = Board(title=title, description=description)
    db.add(new_board)
    await db.commit()
    await db.refresh(new_board)
    return new_board


@router.get("/{board_id}")
async def get_board(board_id: int, db: AsyncSession = Depends(get_db)):
    """Get board by ID"""
    from sqlalchemy import select
    query = select(Board).where(Board.id == board_id)
    result = await db.execute(query)
    board = result.scalars().first()
    
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    
    return board


@router.put("/{board_id}")
async def update_board(board_id: int, title: str, db: AsyncSession = Depends(get_db)):
    """Update board"""
    from sqlalchemy import select
    query = select(Board).where(Board.id == board_id)
    result = await db.execute(query)
    board = result.scalars().first()
    
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    
    board.title = title
    await db.commit()
    await db.refresh(board)
    return board


@router.delete("/{board_id}")
async def delete_board(board_id: int, db: AsyncSession = Depends(get_db)):
    """Delete board"""
    from sqlalchemy import select
    query = select(Board).where(Board.id == board_id)
    result = await db.execute(query)
    board = result.scalars().first()
    
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    
    await db.delete(board)
    await db.commit()
    return {"message": "Board deleted"}
```

---

## Examples

### Complete CRUD Service

Create `app/services/board_service.py`:

```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.board import Board


class BoardService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, title: str, description: str) -> Board:
        """Create a new board"""
        board = Board(title=title, description=description)
        self.db.add(board)
        await self.db.commit()
        await self.db.refresh(board)
        return board

    async def get_all(self) -> list[Board]:
        """Get all active boards"""
        query = select(Board).where(Board.is_active == True)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, board_id: int) -> Board | None:
        """Get board by ID"""
        query = select(Board).where(Board.id == board_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def update(self, board_id: int, **kwargs) -> Board | None:
        """Update board fields"""
        board = await self.get_by_id(board_id)
        if not board:
            return None
        
        for key, value in kwargs.items():
            if hasattr(board, key):
                setattr(board, key, value)
        
        await self.db.commit()
        await self.db.refresh(board)
        return board

    async def delete(self, board_id: int) -> bool:
        """Delete board"""
        board = await self.get_by_id(board_id)
        if not board:
            return False
        
        await self.db.delete(board)
        await self.db.commit()
        return True
```

### Use Service in Routes

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncic import AsyncSession
from app.core.database import get_db
from app.services.board_service import BoardService


router = APIRouter(prefix="/boards", tags=["boards"])


@router.post("/")
async def create_board(title: str, description: str, db: AsyncSession = Depends(get_db)):
    service = BoardService(db)
    return await service.create(title, description)


@router.get("/")
async def list_boards(db: AsyncSession = Depends(get_db)):
    service = BoardService(db)
    return await service.get_all()


@router.get("/{board_id}")
async def get_board(board_id: int, db: AsyncSession = Depends(get_db)):
    service = BoardService(db)
    board = await service.get_by_id(board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return board


@router.put("/{board_id}")
async def update_board(board_id: int, title: str, db: AsyncSession = Depends(get_db)):
    service = BoardService(db)
    board = await service.update(board_id, title=title)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return board


@router.delete("/{board_id}")
async def delete_board(board_id: int, db: AsyncSession = Depends(get_db)):
    service = BoardService(db)
    if not await service.delete(board_id):
        raise HTTPException(status_code=404, detail="Board not found")
    return {"message": "Board deleted"}
```

---

## Initializing Tables

Run this once to create all tables:

```bash
python -c "from app.core.database import create_tables; import asyncio; asyncio.run(create_tables())"
```

Or in your main application startup:

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    await create_tables()
    yield
    # Shutdown code here if needed

app = FastAPI(lifespan=lifespan)
```

---

## Best Practices

1. **Always use `async with AsyncSessionLocal()`** for session management
2. **Use `Depends(get_db)`** in FastAPI routes instead of creating sessions manually
3. **Refresh objects after commit** to get updated data (especially for auto-generated fields)
4. **Use relationships** for cleaner code (e.g., `board.lists` instead of querying)
5. **Implement soft deletes** with `is_active` flag for audit trails
6. **Use services** to centralize database logic
7. **Handle exceptions** appropriately in routes

---

For more information, see [SQLAlchemy Async Documentation](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
