from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.gateway import GatewayStatus, GatewayType
from backend.models.node import NodeGateway
from backend.repositories.interfaces.gateway import (
    IGatewayStatusRepository,
    IGatewayTypeRepository,
    INodeGatewayRepository,
)
from backend.repositories.pagination import Page, Pagination
from backend.repositories.sqlalchemy.base import (
    SQLAlchemyNamedRepository,
    SQLAlchemyRepository,
)


class SQLAlchemyNodeGatewayRepository(
    SQLAlchemyRepository[NodeGateway], INodeGatewayRepository
):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_node(
        self, node_id: UUID, pagination: Pagination = Pagination
    ) -> Page[NodeGateway]:
        stmt = select(NodeGateway).where(NodeGateway.node_id == node_id)
        return await self._paginate(stmt, pagination)

    async def get_by_gateway(
        self, gateway_id: UUID, pagination: Pagination = Pagination
    ) -> Page[NodeGateway]:
        stmt = select(NodeGateway).where(NodeGateway.gateway_id == gateway_id)
        return await self._paginate(stmt, pagination)


class SQLAlchemyGatewayStatusRepository(
    SQLAlchemyNamedRepository[GatewayStatus], IGatewayStatusRepository
):
    def __init__(self, session: AsyncSession):
        self.session = session


class SQLAlchemyGatewayTypeRepository(
    SQLAlchemyNamedRepository[GatewayType], IGatewayTypeRepository
):
    def __init__(self, session: AsyncSession):
        self.session = session
