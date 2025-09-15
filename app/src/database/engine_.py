import asyncio
from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from typing_extensions import AsyncGenerator

from app.config.settings import Settings
from app.logs import Logger
from app.src.exceptions.app_exceptions import AppException

settings = Settings()

#create engine to connect in db
engine = create_async_engine(settings.DB_URL)

#create local session
LocalSession = async_sessionmaker(engine, autoflush=False, expire_on_commit=False)


@asynccontextmanager
async def create_session() -> AsyncGenerator[AsyncSession, Any]:
     async with LocalSession() as db:
          try:
               yield db
          except Exception as e:
               await db.rollback()
               raise e
