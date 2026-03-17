# tests/test_tables.py
import pytest
from app.core.database import create_tables

@pytest.mark.asyncio
async def test_create_tables():
    await create_tables()