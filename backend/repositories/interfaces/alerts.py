from abc import abstractmethod
from datetime import datetime
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
from repositories.interfaces.base import INamedRepository, IRepository

from backend.repositories.pagination import Page, Pagination


class IAlertRepository(IRepository[Alert]):
    @abstractmethod
    async def get_active(
        self, at: datetime, pagination: Pagination = Pagination
    ) -> Page[Alert]: ...

    @abstractmethod
    async def get_by_status(
        self, status_id: UUID, pagination: Pagination = Pagination
    ) -> Page[Alert]: ...

    @abstractmethod
    async def get_by_author(
        self, user_id: UUID, pagination: Pagination = Pagination
    ) -> Page[Alert]: ...

    @abstractmethod
    async def get_by_territory(
        self, territory_id: UUID, pagination: Pagination = Pagination
    ) -> Page[Alert]: ...

    @abstractmethod
    async def search(
        self,
        severity_id: UUID | None = None,
        status_id: UUID | None = None,
        alert_type_id: UUID | None = None,
        pagination: Pagination = Pagination,
    ) -> Page[Alert]: ...


class IAlertVersionRepository(IRepository[AlertVersion]):
    @abstractmethod
    async def get_versions(
        self, alert_id: UUID, pagination: Pagination = Pagination
    ) -> Page[AlertVersion]: ...

    @abstractmethod
    async def get_latest(self, alert_id: UUID) -> AlertVersion | None: ...


class IAlertStatusHistoryRepository(IRepository[AlertStatusHistory]):
    @abstractmethod
    async def get_history(
        self, alert_id: UUID, pagination: Pagination = Pagination
    ) -> Page[AlertStatusHistory]: ...


class IAlertProposalRepository(IRepository[AlertProposal]):
    @abstractmethod
    async def get_pending(
        self, pagination: Pagination = Pagination
    ) -> Page[AlertProposal]: ...

    @abstractmethod
    async def get_by_reviewer(self, reviewer_id: UUID) -> AlertProposal: ...


class IAlertSeverityRepository(IRepository[AlertSeverity]):
    @abstractmethod
    async def get_by_title(self, title: str) -> AlertSeverity: ...  # TODO make seartch


class IAlertTypeRepository(INamedRepository[AlertType]): ...


class IAlertStatusRepository(INamedRepository[AlertStatus]): ...


class IAlertDeliveryStatusRepository(INamedRepository[AlertDeliveryStatus]): ...


class IReviewDecisionRepository(INamedRepository[ReviewDecision]): ...
