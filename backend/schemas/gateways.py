from typing import Any
from uuid import UUID

from pydantic import Field

from .common import Schema, UUIDRead


class GatewayCreate(Schema):
    name: str = Field(min_length=1, max_length=255)
    status_id: UUID
    type_id: UUID
    conf: dict[str, Any] = Field(default_factory=dict)

class GatewayUpdate(Schema):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    status_id: UUID | None = None
    type_id: UUID | None = None
    conf: dict[str, Any] | None = None

class GatewayRead(GatewayCreate, UUIDRead):
    pass

class GatewayStatusRead(UUIDRead):
    name: str
    description: str

class GatewayTypeRead(GatewayStatusRead):
    pass

class ChannelCreate(Schema):
    gateway_id: UUID
    name: str = Field(min_length=1, max_length=255)
    type: str = Field(min_length=1, max_length=50)
    status: str = Field(min_length=1, max_length=30)
    config: dict[str, Any] = Field(default_factory=dict)

class ChannelUpdate(Schema):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    type: str | None = Field(default=None, min_length=1, max_length=50)
    status: str | None = Field(default=None, min_length=1, max_length=30)
    config: dict[str, Any] | None = None

class ChannelRead(ChannelCreate, UUIDRead):
    pass
