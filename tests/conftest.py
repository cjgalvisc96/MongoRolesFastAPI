import asyncio
from typing import Generator, Any

import pytest
from httpx import AsyncClient
from app.core.db import mongo_db
from app.create_app import create_app
from tests.config import settings_test

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().get_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def client() -> Generator:
    async with AsyncClient(app=create_app(settings_test), base_url="http://app.io") as client:
        yield client

@pytest.fixture
def db():
    mongo_db.init_db()
    return mongo_db.db_instance

@pytest.fixture(autouse=True)
async def clean_db(client: AsyncClient, db: Any):
    await db.command("dropDatabase")