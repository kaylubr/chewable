"""Shared pytest fixtures.

Tests run against a dedicated PostgreSQL database (chewables_test) and the
real MinIO bucket, so persistence and object storage are exercised for
real. Storage failure paths are tested by mocking the storage service.
"""
from __future__ import annotations

import os
from collections.abc import AsyncIterator

os.environ["DATABASE_URL"] = (
    "postgresql+asyncpg://chewables:chewables@localhost:5434/chewables_test"
)

import pytest  # noqa: E402
from asgi_lifespan import LifespanManager  # noqa: E402
from httpx import ASGITransport, AsyncClient  # noqa: E402
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine  # noqa: E402

from core.db.base import Base  # noqa: E402
from core.db.session import get_session  # noqa: E402
from core.main import app  # noqa: E402

import core.models  # noqa: E402,F401  (register models on Base.metadata)

engine = create_async_engine(os.environ["DATABASE_URL"])
TestSession = async_sessionmaker(engine, expire_on_commit=False)


async def _reset_schema() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def _session_schema() -> AsyncIterator[None]:
    await _reset_schema()
    yield
    await engine.dispose()


@pytest.fixture(autouse=True)
async def _clean_tables() -> AsyncIterator[None]:
    """Reset rows between tests so each test starts from a clean DB."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


async def _override_get_session() -> AsyncIterator:
    async with TestSession() as session:
        yield session


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    app.dependency_overrides[get_session] = _override_get_session
    transport = ASGITransport(app=app)
    async with LifespanManager(app):
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac
    app.dependency_overrides.clear()
