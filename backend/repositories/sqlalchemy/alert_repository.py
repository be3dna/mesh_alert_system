from uuid import UUID

from models.alert import (
    Alert,
    AlertDeliveryStatus,
    AlertProposal,
    AlertSeverity,
    AlertStatus,
    AlertStatusHistory,
    AlertType,
    AlertVersion,
    ReviewDecision,
)
from repositories.interfaces.alerts import (
    IAlertDeliveryStatusRepository,
    IAlertProposalRepository,
    IAlertRepository,
    IAlertSeverityRepository,
    IAlertStatusHistoryRepository,
    IAlertStatusRepository,
    IAlertTypeRepository,
    IAlertVersionRepository,
    IReviewDecisionRepository,
)
from repositories.pagination import Page, Pagination
from repositories.sqlalchemy.base import (
    SQLAlchemyNamedRepository,
    SQLAlchemyRepository,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class SqlAlchemyAlertRepository(SQLAlchemyRepository[Alert], IAlertRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, alert_id: UUID) -> Alert | None:
        stmt = select(Alert).where(Alert.id == alert_id)

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()


class AlertVersionRepository(
    SQLAlchemyRepository[AlertVersion],
    IAlertVersionRepository,
):
    def __init__(self, session: AsyncSession):
        super().__init__(session, AlertVersion)

    async def get_versions(
        self, alert_id: UUID, pagination: Pagination = Pagination
    ) -> Page[AlertVersion]:
        stmt = (
            select(AlertVersion)
            .where(AlertVersion.alert_id == alert_id)
            .order_by(AlertVersion.alert_version_number.desc())
        )

        return await self._paginate(stmt, pagination)

    async def get_latest(self, alert_id: UUID) -> AlertVersion | None:
        stmt = (
            select(AlertVersion)
            .where(AlertVersion.alert_id == alert_id)
            .order_by(AlertVersion.alert_version_number.desc())
            .limit(1)
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class AlertStatusHistoryRepository(
    SQLAlchemyRepository[AlertStatusHistory],
    IAlertStatusHistoryRepository,
):
    def __init__(self, session: AsyncSession):
        super().__init__(session, AlertStatusHistory)

    async def get_history(
        self, alert_id: UUID, pagination: Pagination = Pagination
    ) -> Page[AlertStatusHistory]:
        stmt = (
            select(AlertStatusHistory)
            .where(AlertStatusHistory.alert_id == alert_id)
            .order_by(
                AlertStatusHistory.changed_at.desc(),
                AlertStatusHistory.id.desc(),
            )
        )

        return await self._paginate(stmt, pagination)


class AlertProposalRepository(
    SQLAlchemyRepository[AlertProposal],
    IAlertProposalRepository,
):
    def __init__(self, session: AsyncSession):
        super().__init__(session, AlertProposal)

    async def get_pending(
        self, pagination: Pagination = Pagination
    ) -> Page[AlertProposal]:
        stmt = (
            select(AlertProposal)
            .where(AlertProposal.reviewed_at.is_(None))
            .order_by(AlertProposal.id)
        )

        return await self._paginate(stmt, pagination)

    async def get_by_reviewer(
        self, reviewer_id: UUID, pagination: Pagination = Pagination
    ) -> Page[AlertProposal]:
        stmt = (
            select(AlertProposal)
            .where(AlertProposal.reviewed_by == reviewer_id)
            .order_by(AlertProposal.reviewed_at.desc())
        )

        return await self._paginate(stmt, pagination)


class AlertSeverityRepository(
    SQLAlchemyRepository[AlertSeverity],
    IAlertSeverityRepository,
):
    def __init__(self, session: AsyncSession):
        super().__init__(session, AlertSeverity)

    async def get_by_title(self, title: str) -> AlertSeverity | None:
        stmt = select(
            AlertSeverity
        ).where(
            AlertSeverity.title == title
        )  # TODO Здесь используется точное совпадение. Для будущего поиска можно добавить отдельный метод search_by_title() с ilike().

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class AlertTypeRepository(
    SQLAlchemyNamedRepository[AlertType],
    IAlertTypeRepository,
):
    def __init__(self, session: AsyncSession):
        super().__init__(session, AlertType)


class AlertStatusRepository(
    SQLAlchemyNamedRepository[AlertStatus],
    IAlertStatusRepository,
):
    def __init__(self, session: AsyncSession):
        super().__init__(session, AlertStatus)


class AlertDeliveryStatusRepository(
    SQLAlchemyNamedRepository[AlertDeliveryStatus],
    IAlertDeliveryStatusRepository,
):
    def __init__(self, session: AsyncSession):
        super().__init__(session, AlertDeliveryStatus)


class ReviewDecisionRepository(
    SQLAlchemyNamedRepository[ReviewDecision],
    IReviewDecisionRepository,
):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ReviewDecision)
