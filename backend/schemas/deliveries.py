from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import Field

from .common import Schema, UUIDRead


class DeliveryRead(UUIDRead):
    alert_id: UUID
    node_id: UUID
    started_at: datetime
    acknowledged_at: datetime | None
    acknowledgement_data: dict[str, Any] | None
    status_id: UUID

class DeliveryStatusRead(UUIDRead):
    name: str
    description: str

class DeliveryAttemptRead(UUIDRead):
    delivery_id: UUID
    attempted_at: datetime
    result: str
    error_reason: str | None

class DeliveryDetail(DeliveryRead):
    attempts: list[DeliveryAttemptRead] = Field(default_factory=list)

class DeliveryRetryRequest(Schema):
    delivery_ids: list[UUID] = Field(min_length=1)
