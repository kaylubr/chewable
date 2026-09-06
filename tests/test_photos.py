"""Backend photo API behavior tests: persistence, ownership, and validation."""
from __future__ import annotations

import io

import pytest
from httpx import AsyncClient
from sqlalchemy import select

from core.models import Photo, User
from core.services.photo import MAX_UPLOAD_BYTES
from tests.conftest import TestSession

PNG_HEADER = b"\x89PNG\r\n\x1a\n"


async def _register(client: AsyncClient, email: str, username: str | None = None) -> dict[str, str]:
    resp = await client.post(
        "/api/auth/register",
        json={
            "email": email,
            "password": "password123",
            "username": username or email.split("@")[0] + "user",
        },
    )
    assert resp.status_code == 201
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _png_bytes(size: int = 64) -> bytes:
    return PNG_HEADER + b"0" * size


async def _upload(client: AsyncClient, headers: dict[str, str], **overrides) -> object:
    data = {"frame": overrides.get("frame", "FILM")}
    content_type = overrides.get("content_type", "image/png")
    body = overrides.get("body", _png_bytes())
    filename = overrides.get("filename", "photo.png")
    return await client.post(
        "/api/photos",
        headers=headers,
        data=data,
        files={"file": (filename, io.BytesIO(body), content_type)},
    )


async def test_photo_create_persists_metadata(client: AsyncClient) -> None:
    headers = await _register(client, "owner@example.com")
    resp = await _upload(client, headers)
    assert resp.status_code == 201
    body = resp.json()
    assert body["frame"] == "FILM"
    assert body["storage_key"].startswith("users/")
    assert body["storage_key"].endswith(".webp")
    assert body["id"]

    async with TestSession() as session:
        photo = (await session.scalars(select(Photo))).first()
        assert photo is not None
        assert str(photo.id) == body["id"]
        assert photo.storage_key == body["storage_key"]
        user = (await session.scalars(select(User))).first()
        assert photo.user_id == user.id


async def test_list_returns_only_current_users_photos(client: AsyncClient) -> None:
    alice = await _register(client, "alice@example.com")
    bob = await _register(client, "bob@example.com")
    await _upload(client, alice)
    await _upload(client, alice)

    bob_list = await client.get("/api/photos", headers=bob)
    assert bob_list.status_code == 200
    assert bob_list.json() == []

    alice_list = await client.get("/api/photos", headers=alice)
    assert alice_list.status_code == 200
    assert len(alice_list.json()) == 2


async def test_users_cannot_fetch_another_users_photo(client: AsyncClient) -> None:
    alice = await _register(client, "alice2@example.com")
    bob = await _register(client, "bob2@example.com")
    created = await _upload(client, alice)
    photo_id = created.json()["id"]

    resp = await client.get(f"/api/photos/{photo_id}/url", headers=bob)
    assert resp.status_code == 404


async def test_users_cannot_delete_another_users_photo(client: AsyncClient) -> None:
    alice = await _register(client, "alice3@example.com")
    bob = await _register(client, "bob3@example.com")
    created = await _upload(client, alice)
    photo_id = created.json()["id"]

    resp = await client.delete(f"/api/photos/{photo_id}", headers=bob)
    assert resp.status_code == 404

    # Alice's photo still exists.
    alice_list = await client.get("/api/photos", headers=alice)
    assert len(alice_list.json()) == 1


async def test_owner_can_delete_photo(client: AsyncClient) -> None:
    headers = await _register(client, "deleter@example.com")
    created = await _upload(client, headers)
    photo_id = created.json()["id"]

    resp = await client.delete(f"/api/photos/{photo_id}", headers=headers)
    assert resp.status_code == 204

    listing = await client.get("/api/photos", headers=headers)
    assert listing.json() == []


async def test_invalid_frame_identifier_rejected(client: AsyncClient) -> None:
    headers = await _register(client, "badframe@example.com")
    resp = await _upload(client, headers, frame="NOT-A-FRAME")
    assert resp.status_code == 422


async def test_unsupported_image_content_type_rejected(client: AsyncClient) -> None:
    headers = await _register(client, "badtype@example.com")
    resp = await _upload(client, headers, content_type="text/plain")
    assert resp.status_code == 422


async def test_empty_upload_rejected(client: AsyncClient) -> None:
    headers = await _register(client, "empty@example.com")
    resp = await _upload(client, headers, body=b"")
    assert resp.status_code == 422


async def test_oversized_upload_rejected(client: AsyncClient) -> None:
    headers = await _register(client, "big@example.com")
    resp = await _upload(client, headers, body=b"0" * (MAX_UPLOAD_BYTES + 1))
    assert resp.status_code == 422


async def test_unauthenticated_upload_rejected(client: AsyncClient) -> None:
    resp = await client.post(
        "/api/photos",
        data={"frame": "FILM"},
        files={"file": ("photo.png", io.BytesIO(_png_bytes()), "image/png")},
    )
    assert resp.status_code == 401
