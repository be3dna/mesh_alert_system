from datetime import datetime
from typing import Any
from uuid import UUID
from pydantic import Field
from .common import Schema, UUIDRead

class SystemEventRead(UUIDRead):
    event_type: str
    registered_at: datetime
    source: str
    user_id: UUID | None
    component_id: str | None
    description: str
    metadata: dict[str, Any] | None = None

class SystemEventFilter(Schema):
    event_type: str | None = None
    source: str | None = None
    from_at: datetime | None = None
    to_at: datetime | None = None

# Settings/backup schemas require an actual settings storage and service contract.
