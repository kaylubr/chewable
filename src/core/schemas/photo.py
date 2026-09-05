"""Photo request/response schemas."""
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PhotoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    frame: str
    storage_key: str
    created_at: datetime
