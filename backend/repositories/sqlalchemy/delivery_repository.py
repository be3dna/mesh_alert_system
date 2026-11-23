

from uuid import UUID

from models.alert import AlertDelivery
from models.delivery_attempt import DeliveryAttempt
from repositories.interfaces.delivery import (
    IAlertDeliveryRepository,
    IDeliveryAttemptRepository,
)
from repositories.pagination import Page, Pagination
from repositories.sqlalchemy.base import SQLAlchemyRepository
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyAlertDeliveryRepository(SQLAlchemyRepository[AlertDelivery],IAlertDeliveryRepository):
   
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_alert(self, alert_id: UUID, pagination:Pagination = Pagination) -> Page[AlertDelivery]:
        stmt = select(AlertDelivery).where(AlertDelivery.alert_id==alert_id).order_by(desc(AlertDelivery.started_at))
        return await self._paginate(stmt, pagination)

    
    async def get_by_alert_and_node(
        self, alert_id: UUID, node_id: UUID
    ) -> AlertDelivery | None:
        stmt = select(AlertDelivery).where(AlertDelivery.alert_id==alert_id, AlertDelivery.node_id==node_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    
    async def get_by_status(self, status_id: UUID, pagination:Pagination = Pagination) -> Page[AlertDelivery]:
        stmt = select(AlertDelivery).where(AlertDelivery.status_id==status_id).order_by(desc(AlertDelivery.started_at))
        return await self._paginate(stmt, pagination)

    async def get_by_status_and_alert(self, alert_id: UUID, status_id:UUID, pagination:Pagination) -> Page[AlertDelivery]:
        stmt = select(AlertDelivery).where(AlertDelivery.alert_id==alert_id, AlertDelivery.status_id==status_id)
        return await self._paginate(stmt, pagination)

    
class SQLAlchemyDeliveryAttemptRepository(SQLAlchemyRepository[DeliveryAttempt],IDeliveryAttemptRepository):
    
    async def get_by_delivery(self, delivery_id: UUID, pagination:Pagination = Pagination) -> Page[DeliveryAttempt]:
        stmt = select(DeliveryAttempt).where(DeliveryAttempt.delivery_id==delivery_id).order_by(desc(DeliveryAttempt.attempted_at))
        return await self._paginate(stmt, pagination)
