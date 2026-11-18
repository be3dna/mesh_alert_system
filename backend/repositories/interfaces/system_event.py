from abc import abstractmethod
from datetime import datetime
from uuid import UUID

from backend.models.system_event import SystemEvent
from backend.repositories.interfaces.base import IRepository


class ISystemEventRepository(IRepository[SystemEvent]):
    @abstractmethod
    async def get_by_period(
        self, start: datetime, end: datetime
    ) -> list[SystemEvent]: ...

    @abstractmethod
    async def get_by_user(self, user_id: UUID) -> list[SystemEvent]: ...

    @abstractmethod
    async def get_by_type(self, type: str) -> list[SystemEvent]: ...
