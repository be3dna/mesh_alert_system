from abc import abstractmethod
from uuid import UUID

from models.territory import Territory
from repositories.interfaces.base import IRepository
from repositories.pagination import Page, Pagination


class ITerritoryRepository(IRepository[Territory]):
    @abstractmethod
    async def find_by_point(
        self, latitude: float, longitude: float, pagination: Pagination = Pagination
    ) -> Page[Territory]: ...

    @abstractmethod
    async def get_alert_territories(
        self, alert_id: UUID, pagination: Pagination = Pagination
    ) -> Page[Territory]: ...

    @abstractmethod
    async def get_geojson(self, territory_id: UUID) -> dict | None: ...
