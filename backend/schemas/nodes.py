from datetime import datetime
from uuid import UUID

from pydantic import Field

from .common import Schema, UUIDRead


class NodeCreate(Schema):
    name: str = Field(min_length=1, max_length=255)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    territory_id: UUID
    status_id: UUID
    external_id: str = Field(min_length=1, max_length=255)

class NodeUpdate(Schema):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    territory_id: UUID | None = None
    status_id: UUID | None = None

class NodeRead(NodeCreate, UUIDRead):
    last_seen_at: datetime

class NodeStatusRead(UUIDRead):
    name: str
    description: str

class NodeGatewayRead(UUIDRead):
    node_id: UUID
    gateway_id: UUID
    last_seen: datetime
