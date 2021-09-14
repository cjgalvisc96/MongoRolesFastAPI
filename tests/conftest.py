import asyncio
from typing import Generator

import pytest
from starlette.testclient import TestClient
from umongo.frameworks import MotorAsyncIOInstance

from app.create_app import create_app
from app.db.session import db_instance
from tests.config import settings_test


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def app(event_loop):
    return create_app(settings_test)


@pytest.fixture
def client(app) -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture
def db():
    return db_instance.db


@pytest.fixture(autouse=True)
async def clean_db(client: TestClient, db: MotorAsyncIOInstance):
    await db.accounts.delete_many({})
