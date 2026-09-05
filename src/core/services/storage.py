"""S3 object-storage service for saved photobooth images.

Local dev uses MinIO (see compose.yml); any S3-compatible endpoint works.
The backend always generates storage keys — clients never choose paths.
"""
from __future__ import annotations

import aioboto3
from botocore.exceptions import ClientError

from core.config import settings


class StorageError(Exception):
    """Raised when an object-storage operation fails."""


class StorageService:
    """Async wrapper around S3 for the chewables bucket."""

    def __init__(self) -> None:
        self._bucket = settings.s3_bucket
        self._session = aioboto3.Session(
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
            region_name=settings.s3_region,
        )

    async def ensure_bucket(self) -> None:
        """Create the bucket if it does not exist (idempotent)."""
        async with self._session.client(
            "s3", endpoint_url=settings.s3_endpoint_url
        ) as s3:
            try:
                await s3.head_bucket(Bucket=self._bucket)
            except ClientError:
                await s3.create_bucket(Bucket=self._bucket)

    async def put(self, key: str, body: bytes, content_type: str) -> None:
        try:
            async with self._session.client(
                "s3", endpoint_url=settings.s3_endpoint_url
            ) as s3:
                await s3.put_object(
                    Bucket=self._bucket,
                    Key=key,
                    Body=body,
                    ContentType=content_type,
                )
        except ClientError as exc:  # pragma: no cover - depends on provider
            raise StorageError(f"object storage put failed for {key}") from exc

    async def delete(self, key: str) -> None:
        try:
            async with self._session.client(
                "s3", endpoint_url=settings.s3_endpoint_url
            ) as s3:
                await s3.delete_object(Bucket=self._bucket, Key=key)
        except ClientError as exc:  # pragma: no cover - depends on provider
            raise StorageError(f"object storage delete failed for {key}") from exc

    async def url(self, key: str) -> str:
        """Return a presigned GET URL for a stored object."""
        try:
            async with self._session.client(
                "s3", endpoint_url=settings.s3_endpoint_url
            ) as s3:
                return await s3.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": self._bucket, "Key": key},
                    ExpiresIn=3600,
                )
        except ClientError as exc:  # pragma: no cover - depends on provider
            raise StorageError(f"object storage url generation failed for {key}") from exc


storage = StorageService()
