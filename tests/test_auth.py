"""Backend auth behavior tests."""
from __future__ import annotations

import pytest
from httpx import AsyncClient
from sqlalchemy import select

from core.models import User
from tests.conftest import TestSession


async def test_register_creates_user_and_returns_token(client: AsyncClient) -> None:
    resp = await client.post(
        "/api/auth/register", json={"email": "user@example.com", "password": "password123"}
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert body["user"]["email"] == "user@example.com"


async def test_password_is_not_stored_in_plaintext(client: AsyncClient) -> None:
    await client.post(
        "/api/auth/register", json={"email": "hash@example.com", "password": "supersecret1"}
    )
    async with TestSession() as session:
        user = (await session.scalars(select(User))).first()
        assert user is not None
        assert user.password_hash != "supersecret1"
        assert user.password_hash.startswith("$argon2")


async def test_duplicate_email_registration_is_rejected(client: AsyncClient) -> None:
    payload = {"email": "dup@example.com", "password": "password123"}
    first = await client.post("/api/auth/register", json=payload)
    assert first.status_code == 201
    second = await client.post("/api/auth/register", json=payload)
    assert second.status_code == 409


async def test_login_succeeds_with_valid_credentials(client: AsyncClient) -> None:
    await client.post(
        "/api/auth/register", json={"email": "login@example.com", "password": "password123"}
    )
    resp = await client.post(
        "/api/auth/login", json={"email": "login@example.com", "password": "password123"}
    )
    assert resp.status_code == 200
    assert resp.json()["access_token"]


async def test_login_fails_with_invalid_password(client: AsyncClient) -> None:
    await client.post(
        "/api/auth/register", json={"email": "badpw@example.com", "password": "password123"}
    )
    resp = await client.post(
        "/api/auth/login", json={"email": "badpw@example.com", "password": "wrong-password"}
    )
    assert resp.status_code == 401


async def test_unauthenticated_user_cannot_access_me(client: AsyncClient) -> None:
    resp = await client.get("/api/auth/me")
    assert resp.status_code == 401


async def test_invalid_token_rejected(client: AsyncClient) -> None:
    resp = await client.get(
        "/api/auth/me", headers={"Authorization": "Bearer not-a-real-token"}
    )
    assert resp.status_code == 401


async def test_me_returns_registered_user(client: AsyncClient) -> None:
    await client.post(
        "/api/auth/register", json={"email": "me@example.com", "password": "password123"}
    )
    login = await client.post(
        "/api/auth/login", json={"email": "me@example.com", "password": "password123"}
    )
    token = login.json()["access_token"]
    resp = await client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["email"] == "me@example.com"


async def test_register_rejects_short_password(client: AsyncClient) -> None:
    resp = await client.post(
        "/api/auth/register", json={"email": "short@example.com", "password": "short"}
    )
    assert resp.status_code == 422


async def test_register_rejects_invalid_email(client: AsyncClient) -> None:
    resp = await client.post(
        "/api/auth/register", json={"email": "not-an-email", "password": "password123"}
    )
    assert resp.status_code == 422
