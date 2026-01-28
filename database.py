from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator

DATABASE_URL = "postgresql+asyncpg://postgres:1234@localhost:5432/test_task"

engine = create_async_engine(DATABASE_URL)
new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        yield session