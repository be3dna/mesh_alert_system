from abc import abstractmethod
from uuid import UUID

from models.alert import AlertDelivery
from models.delivery_attempt import DeliveryAttempt
from repositories.interfaces.base import IRepository


class IAlertDeliveryRepository(IRepository[AlertDelivery]):
    @abstractmethod
    async def get_by_alert(self, alert_id: UUID) -> list[AlertDelivery]: ...

    @abstractmethod
    async def get_by_alert_and_node(
        self, alert_id: UUID, node_id: UUID
    ) -> AlertDelivery | None: ...

    @abstractmethod
    async def get_by_status(self, status_id: UUID) -> list[AlertDelivery]: ...


class IDeliveryAttemptRepository(IRepository[DeliveryAttempt]):
    @abstractmethod
    async def get_by_delivery(self, delivery_id: UUID) -> list[DeliveryAttempt]: ...
