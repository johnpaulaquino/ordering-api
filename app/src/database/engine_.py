from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from typing_extensions import AsyncGenerator

from app.config.settings import Settings
from app.logs import Logger
from app.src.exceptions.app_exceptions import AppException

settings = Settings()

# create engine to connect in db
engine = create_async_engine(
    settings.DB_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_recycle=1800,
)


LocalSession = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)

# Dependency
@asynccontextmanager
async def create_session() -> AsyncGenerator[AsyncSession, Any]:
    async with LocalSession() as db:
        try:
            yield db
        except SQLAlchemyError as e:
            await db.rollback()
            Logger.critical(msg=f"DB error: {e}")
            raise e
        except Exception as e:
            await db.rollback()
            Logger.critical(msg=f"Unexpected error: {e}")
            raise e


from tenacity import retry, stop_after_attempt, wait_fixed


#to retry if encounter error in db
@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
async def safe_execute(db: AsyncSession, stmt, params=None):
    return await db.execute(stmt, params)

#to retry if encounter error in db
@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
async def safe_commit(db: AsyncSession):
    await db.commit()