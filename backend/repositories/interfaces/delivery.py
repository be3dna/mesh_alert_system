from abc import abstractmethod
from uuid import UUID

from models.alert import AlertDelivery
from models.delivery_attempt import DeliveryAttempt
from repositories.interfaces.base import IRepository
from repositories.pagination import Page, Pagination


class IAlertDeliveryRepository(IRepository[AlertDelivery]):
    @abstractmethod
    async def get_by_alert(self, alert_id: UUID, pagination:Pagination = Pagination) -> Page[AlertDelivery]: ...

    @abstractmethod
    async def get_by_alert_and_node(
        self, alert_id: UUID, node_id: UUID
    ) -> AlertDelivery | None: ...

    @abstractmethod
    async def get_by_status(self, status_id: UUID, pagination:Pagination = Pagination) -> Page[AlertDelivery]: ...

    @abstractmethod
    async def get_by_status_and_alert(self, alert_id: UUID, status_id:UUID, pagination:Pagination) -> Page[AlertDelivery]:...
        

class IDeliveryAttemptRepository(IRepository[DeliveryAttempt]):
    @abstractmethod
    async def get_by_delivery(self, delivery_id: UUID, pagination:Pagination = Pagination) -> Page[DeliveryAttempt]: ...
