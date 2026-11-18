from abc import abstractmethod
from uuid import UUID

from models.gateway import GatewayStatus, GatewayType
from models.node import NodeGateway
from repositories.interfaces.base import INamedRepository, IRepository
from repositories.pagination import Page, Pagination


class INodeGatewayRepository(IRepository[NodeGateway]):
    @abstractmethod
    async def get_by_node(
        self, node_id: UUID, pagination: Pagination = Pagination
    ) -> Page[NodeGateway]: ...

    @abstractmethod
    async def get_by_gateway(
        self, gateway_id: UUID, pagination: Pagination = Pagination
    ) -> Page[NodeGateway]: ...


class IGatewayStatusRepository(INamedRepository[GatewayStatus]): ...


class IGatewayTypeRepository(INamedRepository[GatewayType]): ...
