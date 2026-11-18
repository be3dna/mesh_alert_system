import json
from uuid import UUID

from models.territory import AlertTerritory, Territory
from repositories.interfaces.territory import ITerritoryRepository
from repositories.pagination import Page, Pagination
from repositories.sqlalchemy.base import SQLAlchemyRepository
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyTerritoryRepository(
    SQLAlchemyRepository[Territory],
    ITerritoryRepository,
):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Territory)

    async def find_by_point(
        self,
        latitude: float,
        longitude: float,
        pagination: Pagination = Pagination,
    ) -> Page[Territory]:

        point = func.ST_SetSRID(
            func.ST_MakePoint(longitude, latitude),
            4326,
        )

        stmt = (
            select(Territory)
            .where(func.ST_Covers(Territory.geom, point))
            .order_by(Territory.id)
        )

        return await self._paginate(stmt, pagination)

    async def get_alert_territories(
        self,
        alert_id: UUID,
        pagination: Pagination = Pagination,
    ) -> Page[Territory]:

        stmt = (
            select(Territory)
            .join(
                AlertTerritory,
                AlertTerritory.territory_id == Territory.id,
            )
            .where(AlertTerritory.alert_id == alert_id)
            .order_by(Territory.id)
        )

        return await self._paginate(stmt, pagination)

    async def get_geojson(
        self,
        territory_id: UUID,
    ) -> dict | None:

        stmt = (
            select(func.ST_AsGeoJSON(Territory.geom))
            .where(Territory.id == territory_id)
        )

        result = await self.session.execute(stmt)
        geojson = result.scalar_one_or_none()

        if geojson is None:
            return None

        return json.loads(geojson)
