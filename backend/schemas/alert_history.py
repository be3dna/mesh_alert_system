from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import Field

from .common import Schema, UUIDRead


class AlertStatusChange(Schema):
    status_id: UUID
    reason: str = Field(min_length=1)

class AlertStatusHistoryRead(UUIDRead):
    alert_id: UUID
    status_id: UUID
    changed_at: datetime
    reason: str
    changed_by: UUID

class AlertVersionRead(UUIDRead):
    alert_id: UUID
    alert_version_number: int
    previous_version_id: UUID | None
    changed_by: UUID
    changed_at: datetime
    change_reason: str
    snapshot: dict[str, Any]
