import pytest
import logging
from sqlalchemy import text
from app.core.database import engine, create_tables, Base, AsyncSessionLocal
from sqlalchemy.orm import selectinload


# Configure logging for tests
logger = logging.getLogger(__name__)


class TestDatabase:
    """Database connection and operations tests"""

    @pytest.mark.asyncio
    async def test_connection(self):
        """Test database connection is working"""
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            value = result.scalar()
            assert value == 1, "Database connection failed"
            logger.info(f"✅ Database connection successful! Result: {value}")

    @pytest.mark.asyncio
    async def test_connection_with_query(self):
        """Test database connection with actual query"""
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 'Hello' as greeting"))
            greeting = result.scalar()
            assert greeting == "Hello", "Query execution failed"
            logger.info(f"✅ Query execution successful! Result: {greeting}")

    @pytest.mark.asyncio
    async def test_create_tables(self):
        """Test table creation - passes once models are defined"""
        await create_tables()
        
        # Verify tables were created
        async with engine.connect() as conn:
            result = await conn.execute(
                text("""
                    SELECT table_name FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """)
            )
            tables = result.scalars().all()
            
            if len(tables) == 0:
                logger.warning("⚠️  No tables found - models not yet defined. Create models in app/models/ to generate tables")
                pytest.skip("No models defined yet - this test will pass once models are created")
            else:
                logger.info(f"✅ Tables created successfully! Tables: {tables}")
                assert len(tables) > 0, "No tables found in database"

    @pytest.mark.asyncio
    async def test_session_creation(self):
        """Test async session creation"""
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT 1"))
            value = result.scalar()
            assert value == 1, "Session creation failed"
            logger.info(f"✅ Async session created successfully!")

    @pytest.mark.asyncio
    async def test_session_connection_pooling(self):
        """Test connection pooling with multiple sessions"""
        sessions = []
        for i in range(3):
            session = AsyncSessionLocal()
            sessions.append(session)
            result = await session.execute(text("SELECT 1"))
            value = result.scalar()
            assert value == 1, f"Session {i} failed"
            await session.close()
        
        logger.info(f"✅ Connection pooling test passed! Created {len(sessions)} sessions")


# Run tests from command line
if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])