from datetime import datetime
from uuid import UUID

from backend.models.territory import AlertTerritory
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
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession


class SqlAlchemyAlertRepository(SQLAlchemyRepository[Alert], IAlertRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_active(self, at, pagination=Pagination):
        stmt = select(Alert).where(
            Alert.starts_at.between(at, datetime.now()), Alert.ends_at > datetime.now()
        )

        return self._paginate(stmt, pagination)

    async def get_by_status(self, status_id, pagination=Pagination):
        stmt = (
            select(Alert)
            .where(Alert.current_status_id == status_id)
            .order_by(desc(Alert.created_at))
        )

        return self._paginate(stmt, pagination)

    async def get_by_author(self, user_id, pagination=Pagination):
        stmt = (
            select(Alert)
            .where(Alert.created_by == user_id)
            .order_by(desc(Alert.created_at))
        )
        return self._paginate(stmt, pagination)

    async def get_by_territory(self, territory_id, pagination=Pagination):
        stmt = (
            select(Alert)
            .where(Alert.alert_territories.contains(territory_id))
            .order_by(desc(Alert.created_at))
        )
        return self._paginate(stmt, pagination)

    async def search(
        self,
        severity_id: UUID | None = None,
        status_id: UUID | None = None,
        alert_type_id: UUID | None = None,
        starts_from: datetime | None = None,
        starts_to: datetime | None = None,
        territory_id: UUID | None = None,
        is_test: bool | None = None,
        pagination: Pagination | None = None,
    ):
        stmt = select(Alert)

        # Динамическая фильтрация
        if severity_id is not None:
            stmt = stmt.where(Alert.severity_id == severity_id)

        if status_id is not None:
            stmt = stmt.where(Alert.current_status_id == status_id)

        if alert_type_id is not None:
            stmt = stmt.where(Alert.alert_type_id == alert_type_id)

        if starts_from is not None:
            stmt = stmt.where(
                (Alert.ends_at >= starts_from) | (Alert.ends_at.is_(None))
            )

        if starts_to is not None:
            stmt = stmt.where(Alert.starts_at <= starts_to)

        if territory_id is not None:
            stmt = stmt.where(
                Alert.alert_territories.any(AlertTerritory.territory_id == territory_id)
            )
        if is_test is not None:
            stmt = stmt.where(Alert.is_test == is_test)

        count_stmt = select(func.count()).select_from(stmt.order_by(None).subquery())

        total = await self.session.scalar(count_stmt)

        # Сортировка
        stmt = stmt.order_by(Alert.created_at.desc(), Alert.id.desc())

        # Пагинация
        if pagination is not None:
            stmt = stmt.offset(pagination.offset).limit(pagination.limit)

        result = await self.session.scalars(stmt)

        return Page(
            items=result.all(),
            total=total,
            limit=pagination.limit,
            offset=pagination.offset,
        )


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
