from typing import AsyncIterator

from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker

from api.infra.models import BaseModel


class DataBaseContext:
    def __init__(self, dsn: str) -> None:
        self._dsn = dsn
        self._engine: AsyncEngine | None = None
        self._session_maker: async_sessionmaker[AsyncSession] | None = None

    async def __aenter__(self) -> "DataBaseContext":
        self._engine, self._session_maker = await self.init_db(self._dsn)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._engine:
            await self._engine.dispose()

    @staticmethod
    async def init_db(dsn: str) -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
        engine = create_async_engine(dsn, echo=True, pool_size=5, max_overflow=10)

        async with engine.begin() as connection:
            await connection.run_sync(BaseModel.metadata.create_all)

        session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        return engine, session

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        async with self._session_maker() as session:
            async with session.begin():
                yield session
