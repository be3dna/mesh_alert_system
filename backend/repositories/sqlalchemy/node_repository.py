from uuid import UUID

from models.communication_channel import CommunicationChannel
from models.gateway import Gateway
from models.node import Node
from repositories.interfaces.node import (
    ICommunicationChannelRepository,
    IGatewayRepository,
    INodeRepository,
)
from repositories.pagination import Page, Pagination
from repositories.sqlalchemy.base import SQLAlchemyRepository
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyNodeRepository(SQLAlchemyRepository[Node], INodeRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Node)

    async def get_by_external_id(self, external_id: str) -> Node | None:
        stmt = select(Node).where(Node.external_id == external_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_territory(
        self, territory_id: UUID, pagination: Pagination = Pagination
    ) -> Page[Node]:
        stmt = (
            select(Node)
            .where(Node.territory_id == territory_id)
            .order_by(Node.external_id)
        )
        return await self._paginate(stmt, pagination)

    async def get_by_gateway(
        self, gateway_id: UUID, pagination: Pagination = Pagination
    ) -> Page[Node]:
        stmt = (
            select(Node).where(Node.gateway_id == gateway_id).order_by(Node.external_id)
        )
        return await self._paginate(stmt, pagination)


class SQLAlchemyGatewayRepository(SQLAlchemyRepository[Gateway], IGatewayRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_status(
        self, status_id: UUID, pagination: Pagination = Pagination
    ) -> Page[Gateway]:
        stmt = select(Gateway).where(Gateway.status_id == status_id)
        return await self._paginate(stmt, pagination)


class SQLAlchemyCommunicationChannelRepository(
    SQLAlchemyRepository[CommunicationChannel], ICommunicationChannelRepository
):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_gateway(
        self, gateway_id: UUID, pagination: Pagination = Pagination
    ) -> Page[CommunicationChannel]:
        stmt = select(CommunicationChannel).where(
            CommunicationChannel.gateway_id == gateway_id
        )
        return await self._paginate(stmt, pagination)
