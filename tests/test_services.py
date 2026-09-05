"""Service-layer behavior tests: security, frame validation, and failure paths."""
from __future__ import annotations

import io
import uuid

import pytest
from httpx import AsyncClient

from core.frames import FRAME_IDS, is_supported_frame
from core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from core.services.photo import (
    InvalidImageError,
    storage_key_for,
    validate_upload,
)
from tests.test_photos import PNG_HEADER, _png_bytes, _register, _upload


class TestPasswordHashing:
    def test_hash_and_verify_roundtrip(self) -> None:
        hashed = hash_password("correct horse battery staple")
        assert verify_password("correct horse battery staple", hashed) is True
        assert verify_password("wrong", hashed) is False

    def test_same_password_hashes_differ(self) -> None:
        # Argon2 salts each hash; two hashes of one password must not match.
        assert hash_password("same-password") != hash_password("same-password")

    def test_hash_looks_like_argon2(self) -> None:
        assert hash_password("x").startswith("$argon2")


class TestAccessToken:
    def test_roundtrip_user_id(self) -> None:
        uid = uuid.uuid4()
        token = create_access_token(uid)
        assert decode_access_token(token) == uid

    def test_invalid_token_returns_none(self) -> None:
        assert decode_access_token("garbage.token.value") is None

    def test_token_from_other_secret_rejected(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import core.security as security

        monkeypatch.setattr(security.settings, "auth_secret", "another-secret-0123456789abcdef0123456789abcdef")
        other = create_access_token(uuid.uuid4())
        monkeypatch.setattr(security.settings, "auth_secret", "dev-only-change-me-0123456789abcdef0123456789abcdef")
        # Signed with a different key, must not decode.
        assert decode_access_token(other) is None


class TestFrameValidation:
    def test_supported_ids_accepted(self) -> None:
        for frame_id in FRAME_IDS:
            assert is_supported_frame(frame_id) is True

    def test_unknown_ids_rejected(self) -> None:
        assert is_supported_frame("BOGUS") is False
        assert is_supported_frame("") is False
        assert is_supported_frame("film") is False  # case-sensitive


class TestUploadValidation:
    def test_accepts_valid_image_types(self) -> None:
        for ct in ("image/jpeg", "image/png", "image/webp"):
            validate_upload(ct, 100)

    def test_rejects_invalid_content_type(self) -> None:
        with pytest.raises(InvalidImageError):
            validate_upload("text/html", 100)

    def test_rejects_empty_and_oversized(self) -> None:
        with pytest.raises(InvalidImageError):
            validate_upload("image/png", 0)
        from core.services.photo import MAX_UPLOAD_BYTES

        with pytest.raises(InvalidImageError):
            validate_upload("image/png", MAX_UPLOAD_BYTES + 1)


class TestStorageKey:
    def test_key_is_server_generated_and_scoped(self) -> None:
        uid = uuid.uuid4()
        pid = uuid.uuid4()
        key = storage_key_for(uid, pid)
        assert key == f"users/{uid}/photos/{pid}.webp"
        assert ".." not in key  # no path traversal from client input
