from abc import abstractmethod
from datetime import datetime
from uuid import UUID

from models.system_event import SystemEvent
from repositories.interfaces.base import IRepository
from repositories.pagination import Page, Pagination


class ISystemEventRepository(IRepository[SystemEvent]):
    @abstractmethod
    async def get_by_period(
        self, start: datetime, end: datetime, pagination: Pagination = Pagination
    ) -> Page[SystemEvent]: ...

    @abstractmethod
    async def get_by_user(
        self, user_id: UUID, pagination: Pagination = Pagination
    ) -> Page[SystemEvent]: ...

    @abstractmethod
    async def get_by_type(
        self, event_type: str, pagination: Pagination = Pagination
    ) -> Page[SystemEvent]: ...
