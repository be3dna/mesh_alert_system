from abc import abstractmethod
from uuid import UUID

from backend.models.gateway import GatewayStatus, GatewayType
from backend.repositories.interfaces.base import INamedRepository, IRepository


class INodeGatewayRepository(IRepository):
    @abstractmethod
    async def get_by_node(self, node_id: UUID): ...
    @abstractmethod
    async def get_by_gateway(self, gateway_id: UUID): ...


class IGatewayStatusRepository(INamedRepository[GatewayStatus]): ...


class IGatewayTypeRepository(INamedRepository[GatewayType]): ...
