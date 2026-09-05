"""Storage failure paths: partial operations must not leave inconsistent state."""
from __future__ import annotations

import pytest
from httpx import AsyncClient
from sqlalchemy import select

from core.models import Photo, User
from core.services import photo as photo_service
from core.services.storage import StorageError
from tests.conftest import TestSession
from tests.test_photos import _register, _upload


async def test_storage_failure_on_create_leaves_no_photo_record(
    client: AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    headers = await _register(client, "storefail@example.com")

    async def boom(*args, **kwargs) -> None:
        raise StorageError("simulated outage")

    monkeypatch.setattr(photo_service.storage, "put", boom)
    resp = await _upload(client, headers)
    assert resp.status_code == 503

    async with TestSession() as session:
        photos = (await session.scalars(select(Photo))).all()
        assert photos == []


async def test_delete_storage_failure_keeps_record(
    client: AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    headers = await _register(client, "delfail@example.com")
    created = await _upload(client, headers)
    photo_id = created.json()["id"]
    assert created.status_code == 201

    async def boom(*args, **kwargs) -> None:
        raise StorageError("simulated outage")

    monkeypatch.setattr(photo_service.storage, "delete", boom)
    resp = await client.delete(f"/api/photos/{photo_id}", headers=headers)
    assert resp.status_code == 503

    # Row survives because the object still exists in storage.
    async with TestSession() as session:
        photos = (await session.scalars(select(Photo))).all()
        assert len(photos) == 1


async def test_db_commit_failure_after_put_removes_stored_object(
    client: AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A failed DB commit after the object was stored must not orphan the object."""
    from sqlalchemy.ext.asyncio import AsyncSession

    headers = await _register(client, "dbfail@example.com")
    async with TestSession() as session:
        user = (await session.scalars(select(User))).first()

    deleted_keys: list[str] = []
    real_put = photo_service.storage.put
    real_delete = photo_service.storage.delete

    async def recording_put(key: str, body: bytes, content_type: str) -> None:
        await real_put(key, body, content_type)

    async def recording_delete(key: str) -> None:
        deleted_keys.append(key)
        await real_delete(key)

    monkeypatch.setattr(photo_service.storage, "put", recording_put)
    monkeypatch.setattr(photo_service.storage, "delete", recording_delete)

    original_commit = AsyncSession.commit

    async def failing_commit(self) -> None:
        raise RuntimeError("simulated db failure")

    AsyncSession.commit = failing_commit  # type: ignore[method-assign]
    try:
        async with TestSession() as session:
            with pytest.raises(RuntimeError):
                await photo_service.create_photo(
                    session=session,
                    user=user,
                    frame="FILM",
                    image_bytes=b"\x89PNG\r\n\x1a\n" + b"0" * 64,
                    content_type="image/png",
                )
    finally:
        AsyncSession.commit = original_commit  # type: ignore[method-assign]

    assert deleted_keys, "cleanup delete should have run"
    async with TestSession() as session:
        photos = (await session.scalars(select(Photo))).all()
        assert photos == []
