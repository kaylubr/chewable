"""Supported frame identifiers, shared with the frontend-owned vocabulary.

The backend does not know how a frame renders — it only validates that a
persisted photo's frame identifier is one of these supported values.
"""
from typing import Literal

FRAME_IDS = ("VINTAGE", "POLAROID", "FILM", "CLASSIC")

FrameId = Literal["VINTAGE", "POLAROID", "FILM", "CLASSIC"]


def is_supported_frame(frame: str) -> bool:
    return frame in FRAME_IDS
