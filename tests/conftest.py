import pytest_asyncio
from datetime import datetime

from db.database import Base, test_session_factory, test_engine
from db.models import User, Task


@pytest_asyncio.fixture(scope="function")
async def session():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    session = test_session_factory()
    session.begin()
    session.add_all(
        [
            User(id=42, username="@bob"),
            User(id=24, username="@tom"),
            Task(text="hello", due=datetime(2002, 10, 1), user_id=42),
            Task(text="by", due=datetime(2100, 10, 1), user_id=42),
            Task(id = 123, text="hi", due=datetime(2025, 12, 1), user_id=24),
        ]
    )
    await session.commit()
    yield session
    await session.close()
    await test_engine.dispose()
