from datetime import datetime
from enum import StrEnum


class ReferenceState(StrEnum):
    CREATED = "created"
    UPDATED = "updated"

    @classmethod
    def from_timestamps(cls, created_at: datetime, updated_at: datetime) -> "ReferenceState":
        return cls.UPDATED if updated_at > created_at else cls.CREATED
