from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.alert import Alert

class SqlAlchemyAlertRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, alert_id:UUID) -> Alert|None:
        stmt = select(Alert).where(
            Alert.id == alert_id
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()
