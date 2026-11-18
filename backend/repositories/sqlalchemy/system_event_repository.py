
from datetime import datetime
from uuid import UUID

from models.system_event import SystemEvent
from repositories.interfaces.system_event import ISystemEventRepository
from repositories.pagination import Page, Pagination
from repositories.sqlalchemy.base import SQLAlchemyRepository
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession


class SQLALchemySystemEventRepository(SQLAlchemyRepository[SystemEvent], ISystemEventRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_period(
        self, start: datetime, end: datetime, pagination: Pagination = Pagination
    ) -> Page[SystemEvent]: 
    
        stmt = select(SystemEvent).where(SystemEvent.registered_at.between(start, end)).order_by(desc(SystemEvent.registered_at))
        return await self._paginate(stmt, pagination)


    async def get_by_user(
        self, user_id: UUID, pagination: Pagination = Pagination
    ) -> Page[SystemEvent]:
            stmt = select(SystemEvent).where(SystemEvent.user_id == user_id).order_by(desc(SystemEvent.registered_at))
            return await self._paginate(stmt, pagination)
        

    async def get_by_type(
        self, event_type: str, pagination: Pagination = Pagination
    ) -> Page[SystemEvent]: 
            stmt = select(SystemEvent).where(SystemEvent.event_type == event_type).order_by(desc(SystemEvent.registered_at))
            return await self._paginate(stmt, pagination)
