import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.api.deps import get_current_user
from core.db.session import get_session
from core.frames import FRAME_IDS
from core.models import Photo, User
from core.schemas.photo import PhotoOut
from core.services.photo import (
    InvalidFrameError,
    InvalidImageError,
    PhotoNotFoundError,
    StorageError as PhotoStorageError,
    create_photo,
    delete_photo,
    get_owned_photo,
    list_user_photos,
)
from core.services.storage import StorageError, storage

router = APIRouter(prefix="/photos", tags=["photos"])


def _not_found() -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")


@router.post("", response_model=PhotoOut, status_code=status.HTTP_201_CREATED)
async def upload_photo(
    frame: str = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> PhotoOut:
    """Save the composed photobooth image for the current user."""
    if frame not in FRAME_IDS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Unsupported frame identifier: {frame!r}",
        )
    image_bytes = await file.read()
    try:
        photo = await create_photo(
            session,
            user=current_user,
            frame=frame,
            image_bytes=image_bytes,
            content_type=file.content_type or "",
        )
    except InvalidFrameError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Unsupported frame identifier: {frame!r}",
        ) from None
    except InvalidImageError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(exc),
        ) from None
    except StorageError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not store the image; please try again",
        ) from None
    return PhotoOut.model_validate(photo)


@router.get("", response_model=list[PhotoOut])
async def list_photos(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> list[PhotoOut]:
    photos = await list_user_photos(session, current_user.id)
    return [PhotoOut.model_validate(p) for p in photos]


@router.get("/{photo_id}/url", response_model=dict[str, str])
async def photo_url(
    photo_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict[str, str]:
    """Return a short-lived URL for the photo after verifying ownership."""
    try:
        photo = await get_owned_photo(session, current_user.id, photo_id)
    except PhotoNotFoundError:
        raise _not_found() from None
    try:
        url = await storage.url(photo.storage_key)
    except StorageError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not retrieve the image; please try again",
        ) from None
    return {"url": url}


@router.delete("/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_photo(
    photo_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    try:
        photo = await get_owned_photo(session, current_user.id, photo_id)
    except PhotoNotFoundError:
        raise _not_found() from None
    try:
        await delete_photo(session, photo)
    except PhotoStorageError:
        # Storage deletion failed — do not delete the DB row for an object
        # that still exists; surface a safe error.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not delete the image; please try again",
        ) from None
