from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from .env file"""
    database_url: str = Field(
        default="postgresql+asyncpg://user:password@localhost:5432/trello_db",
        alias="DATABASE_URL"
    )
    sql_echo: bool = Field(default=False, alias="SQL_ECHO")
    environment: str = Field(default="development", alias="ENVIRONMENT")

    class Config:
        env_file = ".env"


# Load settings
settings = Settings()

# Create async engine with SQLAlchemy 2.0
engine = create_async_engine(
    settings.database_url,
    echo=settings.sql_echo,
    pool_pre_ping=True,  # Test connections before using them
    poolclass=NullPool if settings.environment == "development" else None,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


# Base class for all models
class Base(DeclarativeBase):
    pass


# Async dependency for FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session for FastAPI dependency injection"""
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