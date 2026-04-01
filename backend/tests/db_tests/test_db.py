import pytest
import logging
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import pytest_asyncio

from app.core.database import engine, Base, AsyncSessionLocal

logger = logging.getLogger(__name__)


# -----------------------------
# FIXTURE: DB setup/teardown
# -----------------------------
@pytest_asyncio.fixture(scope="function")
async def db() -> AsyncSession:
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Provide session
    async with AsyncSessionLocal() as session:
        yield session

    # Drop tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        
        
# -----------------------------
# TESTS
# -----------------------------
@pytest.mark.asyncio
class TestDatabase:
    """Database connection and operations tests"""

    async def test_connection(self):
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            assert result.scalar() == 1

    async def test_basic_query(self):
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 'Hello'"))
            assert result.scalar() == "Hello"

    async def test_tables_created(self, db: AsyncSession):
        """
        Verify tables are registered in SQLAlchemy metadata.
        """
        tables = Base.metadata.tables.keys()
        assert "boards" in tables
        assert "lists" in tables
        assert "cards" in tables
        logger.info(f"✅ Tables registered: {tables}")

    async def test_session_creation(self, db: AsyncSession):
        """
        Verify async session works.
        """
        result = await db.execute(text("SELECT 1"))
        assert result.scalar() == 1

    async def test_multiple_sessions(self):
        """
        Create and test multiple AsyncSessions.
        """
        sessions = []

        for _ in range(3):
            async with AsyncSessionLocal() as session:
                result = await session.execute(text("SELECT 1"))
                assert result.scalar() == 1
                sessions.append(session)

        logger.info("✅ Multiple session test passed")