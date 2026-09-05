"""Photo business logic: save, list, fetch, and delete saved photos.

A saved photo is the final composed photobooth image uploaded by an
authenticated user. The image goes to object storage under a server-
generated key; only metadata lives in Postgres. Every operation enforces
ownership — the current user comes from the auth mechanism, never from a
client-supplied id.
"""
from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.frames import is_supported_frame
from core.models import Photo, User
from core.services.storage import StorageError, storage

# Upload validation
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_UPLOAD_BYTES = 20 * 1024 * 1024  # 20 MB


class InvalidFrameError(Exception):
    pass


class InvalidImageError(Exception):
    pass


class PhotoNotFoundError(Exception):
    pass


def storage_key_for(user_id: uuid.UUID, photo_id: uuid.UUID) -> str:
    """Server-generated key; clients never choose storage paths."""
    return f"users/{user_id}/photos/{photo_id}.webp"


def validate_upload(content_type: str | None, size: int) -> None:
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise InvalidImageError(
            f"unsupported content type {content_type!r}; "
            f"expected one of {sorted(ALLOWED_CONTENT_TYPES)}"
        )
    if size <= 0:
        raise InvalidImageError("empty upload")
    if size > MAX_UPLOAD_BYTES:
        raise InvalidImageError(f"upload exceeds {MAX_UPLOAD_BYTES} byte limit")


async def create_photo(
    session: AsyncSession,
    *,
    user: User,
    frame: str,
    image_bytes: bytes,
    content_type: str,
) -> Photo:
    """Validate, store, and record a photo; clean up on failure."""
    if not is_supported_frame(frame):
        raise InvalidFrameError(f"unsupported frame identifier: {frame!r}")
    validate_upload(content_type, len(image_bytes))

    photo_id = uuid.uuid4()
    key = storage_key_for(user.id, photo_id)

    try:
        await storage.put(key, image_bytes, content_type)
    except StorageError:
        # Nothing persisted yet — nothing to clean up.
        raise

    photo = Photo(id=photo_id, user_id=user.id, frame=frame, storage_key=key)
    session.add(photo)
    try:
        await session.commit()
    except Exception:
        # Do not leave an orphaned object if the DB write fails.
        await session.rollback()
        try:
            await storage.delete(key)
        except StorageError:
            pass
        raise
    await session.refresh(photo)
    return photo


async def list_user_photos(
    session: AsyncSession, user_id: uuid.UUID
) -> list[Photo]:
    result = await session.scalars(
        select(Photo).where(Photo.user_id == user_id).order_by(Photo.created_at.desc())
    )
    return list(result)


async def get_owned_photo(
    session: AsyncSession, user_id: uuid.UUID, photo_id: uuid.UUID
) -> Photo:
    """Fetch a photo only if it belongs to the user, else raise."""
    photo = await session.get(Photo, photo_id)
    if photo is None or photo.user_id != user_id:
        raise PhotoNotFoundError()
    return photo


async def delete_photo(session: AsyncSession, photo: Photo) -> None:
    """Delete the object-storage image and the DB row."""
    await storage.delete(photo.storage_key)
    await session.delete(photo)
    await session.commit()
