from typing import AsyncGenerator
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from .env file"""

    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/trello_db",
        alias="DATABASE_URL"
    )
    sql_echo: bool = Field(default=False, alias="SQL_ECHO")
    environment: str = Field(default="development", alias="ENVIRONMENT")

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parents[2] / ".env",
        env_file_encoding="utf-8"
    )


# Load settings from .env
settings = Settings()


# Create async SQLAlchemy engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.sql_echo,
    pool_pre_ping=True,
    poolclass=NullPool if settings.environment == "development" else None,
)


# Async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


# Base class for ORM models
class Base(DeclarativeBase):
    pass


# FastAPI dependency for DB sessions
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Provide a database session for FastAPI dependencies"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# Function to create all tables
async def create_tables() -> None:
    """Create all tables in the database"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Function to drop all tables
async def drop_tables() -> None:
    """Drop all tables from the database"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)