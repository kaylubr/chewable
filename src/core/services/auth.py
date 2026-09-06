"""Auth business logic: registration, login, and token-based user resolution."""
from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from core.schemas.auth import RegisterRequest
from core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


class EmailTakenError(Exception):
    pass


class UsernameTakenError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


async def register_user(session: AsyncSession, req: RegisterRequest) -> User:
    user = User(
        username=req.username,
        email=str(req.email).lower(),
        password_hash=hash_password(req.password),
    )
    session.add(user)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise await _conflict_error(session, req) from None
    await session.refresh(user)
    return user


async def _conflict_error(
    session: AsyncSession, req: RegisterRequest
) -> EmailTakenError | UsernameTakenError:
    """Distinguish which unique constraint collided after an IntegrityError."""
    email_taken = await session.scalar(
        select(User.id).where(User.email == str(req.email).lower())
    )
    if email_taken is not None:
        return EmailTakenError()
    return UsernameTakenError()


async def authenticate_user(
    session: AsyncSession, username: str, password: str
) -> User:
    user = await session.scalar(select(User).where(User.username == username))
    if user is None or not verify_password(password, user.password_hash):
        raise InvalidCredentialsError()
    return user


def issue_token(user: User) -> str:
    return create_access_token(user.id)


async def user_from_token(session: AsyncSession, token: str) -> User | None:
    user_id = decode_access_token(token)
    if user_id is None:
        return None
    return await session.get(User, user_id)


async def get_user_by_id(session: AsyncSession, user_id: uuid.UUID) -> User | None:
    return await session.get(User, user_id)
