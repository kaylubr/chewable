"""User model.

Authentication exists only so a user can permanently save finished photos.
Guests never touch this table.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db.base import Base

if TYPE_CHECKING:
    from core.models.oauth_identity import OAuthIdentity
    from core.models.photo import Photo


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(
        String(32), unique=True, index=True, nullable=False
    )
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    photos: Mapped[list[Photo]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    oauth_identities: Mapped[list[OAuthIdentity]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
