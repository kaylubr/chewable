"""Backend auth behavior tests."""
from __future__ import annotations

import pytest
from httpx import AsyncClient
from sqlalchemy import select

from core.models import User
from tests.conftest import TestSession


async def test_register_creates_user_and_returns_token(client: AsyncClient) -> None:
    resp = await client.post(
        "/api/auth/register",
        json={"email": "user@example.com", "password": "password123", "username": "user"},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert body["user"]["email"] == "user@example.com"
    assert body["user"]["username"] == "user"


async def test_password_is_not_stored_in_plaintext(client: AsyncClient) -> None:
    await client.post(
        "/api/auth/register",
        json={"email": "hash@example.com", "password": "supersecret1", "username": "hashuser"},
    )
    async with TestSession() as session:
        user = (await session.scalars(select(User))).first()
        assert user is not None
        assert user.password_hash != "supersecret1"
        assert user.password_hash.startswith("$argon2")


async def test_duplicate_email_registration_is_rejected(client: AsyncClient) -> None:
    payload = {"email": "dup@example.com", "password": "password123", "username": "dupuser"}
    first = await client.post("/api/auth/register", json=payload)
    assert first.status_code == 201
    second = await client.post("/api/auth/register", json=payload)
    assert second.status_code == 409


async def test_duplicate_username_registration_is_rejected(client: AsyncClient) -> None:
    first = await client.post(
        "/api/auth/register",
        json={"email": "one@example.com", "password": "password123", "username": "sameuser"},
    )
    assert first.status_code == 201
    second = await client.post(
        "/api/auth/register",
        json={"email": "two@example.com", "password": "password123", "username": "sameuser"},
    )
    assert second.status_code == 409


async def test_register_rejects_username_with_bad_characters(client: AsyncClient) -> None:
    for bad in ["has space", "has/slash", "UPPER", "", "ab"]:
        resp = await client.post(
            "/api/auth/register",
            json={"email": "bad@example.com", "password": "password123", "username": bad},
        )
        assert resp.status_code == 422


async def test_login_succeeds_with_username(client: AsyncClient) -> None:
    await client.post(
        "/api/auth/register",
        json={
            "email": "login@example.com",
            "password": "password123",
            "username": "loginuser",
        },
    )
    # ADR 0005: username is the login identifier.
    resp = await client.post(
        "/api/auth/login", json={"username": "loginuser", "password": "password123"}
    )
    assert resp.status_code == 200
    assert resp.json()["access_token"]
    assert resp.json()["user"]["username"] == "loginuser"


async def test_login_fails_with_invalid_password(client: AsyncClient) -> None:
    await client.post(
        "/api/auth/register",
        json={"email": "badpw@example.com", "password": "password123", "username": "badpwuser"},
    )
    resp = await client.post(
        "/api/auth/login", json={"username": "badpwuser", "password": "wrong-password"}
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
        "/api/auth/register",
        json={"email": "me@example.com", "password": "password123", "username": "meuser"},
    )
    login = await client.post(
        "/api/auth/login", json={"username": "meuser", "password": "password123"}
    )
    token = login.json()["access_token"]
    resp = await client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["email"] == "me@example.com"
    assert resp.json()["username"] == "meuser"


async def test_register_rejects_short_password(client: AsyncClient) -> None:
    resp = await client.post(
        "/api/auth/register",
        json={"email": "short@example.com", "password": "short", "username": "shortuser"},
    )
    assert resp.status_code == 422


async def test_register_rejects_invalid_email(client: AsyncClient) -> None:
    resp = await client.post(
        "/api/auth/register",
        json={"email": "not-an-email", "password": "password123", "username": "bademail"},
    )
    assert resp.status_code == 422


async def test_register_rejects_missing_username(client: AsyncClient) -> None:
    resp = await client.post(
        "/api/auth/register", json={"email": "nouser@example.com", "password": "password123"}
    )
    assert resp.status_code == 422
