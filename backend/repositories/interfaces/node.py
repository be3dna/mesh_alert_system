from abc import abstractmethod
from uuid import UUID

from models.communication_channel import CommunicationChannel
from models.gateway import Gateway
from models.node import Node
from repositories.interfaces.base import IRepository
from repositories.pagination import Page, Pagination


class INodeRepository(IRepository[Node]):
    @abstractmethod
    async def get_by_external_id(self, external_id: str) -> Node | None: ...

    @abstractmethod
    async def get_by_territory(
        self, territory_id: UUID, pagination: Pagination = Pagination
    ) -> Page[Node]: ...

    @abstractmethod
    async def get_by_gateway(
        self, gateway_id: UUID, pagination: Pagination = Pagination
    ) -> Page[Node]: ...


class IGatewayRepository(IRepository[Gateway]):
    @abstractmethod
    async def get_by_status(
        self, status_id: UUID, pagination: Pagination = Pagination
    ) -> Page[Gateway]: ...


class ICommunicationChannelRepository(IRepository[CommunicationChannel]):
    @abstractmethod
    async def get_by_gateway(
        self, gateway_id: UUID, pagination: Pagination = Pagination
    ) -> Page[CommunicationChannel]: ...
