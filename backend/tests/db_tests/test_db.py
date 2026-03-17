import pytest
import asyncio
from sqlalchemy import text
from app.core.database import engine, create_tables

@pytest.mark.asyncio
async def test_connection():
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            value = result.scalar()
            print("Connection successful! Result:", value)
    except Exception as e:
        print("Connection failed:", str(e))

@pytest.mark.asyncio
async def test_create_tables():
    try:
        await create_tables()
        print("Tables created successfully!")
    except Exception as e:
        print("Table creation failed:", str(e))

async def main():
    await test_connection()
    await test_create_tables()

if __name__ == "__main__":
    asyncio.run(main())