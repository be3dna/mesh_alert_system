from typing import Protocol
from uuid import UUID

from models.alert import Alert


class AlertRepository(Protocol):
    async def get_by_id(self, alert_id: UUID) -> Alert | None: ...
