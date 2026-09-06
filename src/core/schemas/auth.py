"""Auth request/response schemas."""
import re
import uuid

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

USERNAME_PATTERN = re.compile(r"^[a-z0-9_]{3,32}$")


class RegisterRequest(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=32)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not USERNAME_PATTERN.match(value):
            raise ValueError(
                "Username must be 3-32 characters: lowercase letters, digits, underscores"
            )
        return value


class LoginRequest(BaseModel):
    # Username is the login identifier (ADR 0005); email login is not supported.
    username: str = Field(min_length=3, max_length=32)
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: EmailStr
    username: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
