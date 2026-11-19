from uuid import UUID

from core.exceptions import (
    AlertNotFoundError,
    InvalidTerritoryError,
    StatusNotFoundError,
    UserNotFoundError,
)
from models.alert import Alert, AlertProposal, AlertStatusHistory, AlertVersion
from models.territory import AlertTerritory
from repositories.interfaces.alerts import (
    IAlertProposalRepository,
    IAlertRepository,
    IAlertStatusHistoryRepository,
    IAlertStatusRepository,
    IAlertVersionRepository,
    IReviewDecisionRepository,
)
from repositories.interfaces.territory import ITerritoryRepository
from repositories.interfaces.users import IRoleRepository, IUserRepository
from repositories.pagination import Page, Pagination
from schemas.alert import AlertCreate, AlertFilters, AlertSnapshot, AlertUpdate
from schemas.proposals import ProposalCreate, ProposalReview
from services.premission_service import PermissionDeniedError, PermissionService
from services.premissions import Permission
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession


class AlertService:
    def __init__(
        self,
        session: AsyncSession,
        repository: IAlertRepository,
        users: IUserRepository,
        roles: IRoleRepository,
        statusts: IAlertStatusRepository,
        decisions: IReviewDecisionRepository,
        history: IAlertStatusHistoryRepository,
        versions: IAlertVersionRepository,
        premissions: PermissionService,
        proposal: IAlertProposalRepository,
        territories: ITerritoryRepository,
    ):
        self.session = session
        self.repository = repository
        self.users = users
        self.roles = roles
        self.statuses = statusts
        self.decisions = decisions
        self.history = history
        self.versions = versions
        self.permissions = premissions
        self.proposals = proposal
        self.territories = territories
    
    @staticmethod
    def _build_alert_snapshot(
        alert: Alert,
        territory_ids: list[UUID],
    ) -> dict:
        return AlertSnapshot(
            title=alert.title,
            description=alert.description,
            severity_id=alert.severity_id,
            alert_type_id=alert.alert_type_id,
            starts_at=alert.starts_at,
            ends_at=alert.ends_at,
            is_test=alert.is_test,
            territory_ids=territory_ids,
        ).model_dump(mode="json")

    async def create_alert(self, data: AlertCreate, actor_id: UUID) -> Alert:
        async with self.session.begin():
            actor = await self.users.get_by_id(actor_id)

            if actor is None:
                raise UserNotFoundError(actor_id)

            can_create = self.permissions.has_permission(
                actor.role.name,
                Permission.ALERT_CREATE,
            )

            can_propose = self.permissions.has_permission(
                actor.role.name,
                Permission.ALERT_PROPOSE,
            )

            if not can_create and not can_propose:
                raise PermissionDeniedError()

            requires_review = not can_create
            status_name = "pending_review" if requires_review else "created"
            status = await self.statuses.get_by_name(status_name)

            alert = Alert(
                title=data.title,
                description=data.description,
                severity_id=data.severity_id,
                alert_type_id=data.alert_type_id,
                created_by=actor_id,
                current_status_id=status.id,
                starts_at=data.starts_at,
                ends_at=data.ends_at,
                is_test=data.is_test,
            )

            await self.repository.add(alert)
            await self.session.flush()

            if requires_review:
                decision = await self.decisions.get_by_name("proposed")
                proposal = AlertProposal(
                    alert_id=alert.id,
                    decision_id=decision.id,
                    reviewed_by=None,
                    reviewed_at=None,
                    review_comment=None,
                )
                await self.proposals.add(proposal)

            alert_history_note = AlertStatusHistory(
                alert_id=alert.id,
                status_id=status.id,
                reason="creation",
                changed_by=actor_id,
            )

            await self.history.add(alert_history_note)

            territory_ids = set(data.territory_ids)

            territories = await self.territories.get_by_ids(list(territory_ids))

            if len(territories) != len(territory_ids):
                raise InvalidTerritoryError()

            alert.territories = territories

            snapshot = self._build_alert_snapshot(
                alert,
                territory_ids,
            )

            alert_version = AlertVersion(
                alert_id=alert.id,
                alert_version_number=1,
                previous_version_id=None,
                changed_by=actor_id,
                change_reason="creation",
                snapshot=snapshot,
            )

            await self.versions.add(alert_version)

        return alert

    async def get_alert(self, alert_id: UUID) -> Alert:
        alert = await self.repository.get_by_id(alert_id)

        if alert is None:
            raise AlertNotFoundError(alert_id)

        await self.session.refresh(
            alert,
            [
                "alert_territories",
                "creator",
                "current_status",
                "severity",
                "alert_type",
                "versions",
                "deliveries",
                "proposal",
                "alert_statuses_history",
            ],
        )
        return alert

    async def get_alerts(
        self, filters: AlertFilters, pagination: Pagination = Pagination
    ) -> Page[Alert]:
        page = await self.repository.search(
            severity_id=filters.severity_id,
            status_id=filters.status_id,
            alert_type_id=filters.alert_type_id,
            territory_id=filters.territory_id,
            starts_from=filters.period_from,
            starts_to=filters.period_to,
            is_test=filters.is_test,
            pagination=pagination,
        )
        return page

    async def update_territories(
        self,
        alert_id: UUID,
        territories_ids: list[UUID],
    ):
        await self.session.execute(
            delete(AlertTerritory).where(AlertTerritory.alert_id == alert_id)
        )

        self.session.add_all(
            [
                AlertTerritory(
                    alert_id=alert_id,
                    territory_id=territory_id,
                )
                for territory_id in set(territories_ids)
            ]
        )

    async def update_alert(
        self, alert_id: UUID, data: AlertUpdate, actor_id: UUID
    ) -> Alert:
        actor = await self.users.get_by_id(actor_id)

        if actor is None:
            raise UserNotFoundError(actor_id)

        can_udpate = self.permissions.has_permission(
            actor.role.name,
            Permission.ALERT_UPDATE,
        )
        can_update_any = self.permissions.has_permission(
            actor.role.name, Permission.ALERT_UPDATE_ANY
        )

        if not can_udpate and not can_update_any:
            raise PermissionDeniedError()

        alert = await self.repository.get_by_id(alert_id)

        if alert is None:
            raise AlertNotFoundError(alert_id)

        if alert.created_by != actor_id and not can_update_any:
            raise PermissionDeniedError()

        update_data = data.model_dump(exclude_unset=True)

        territories_ids = update_data.pop("territories_id", None)
        change_reason = update_data.pop("change_reason", None)

        for field, value in update_data.items():
            setattr(alert, field, value)

        if territories_ids is not None:
            await self.update_territories(alert_id, territories_ids)

        await self.session.flush()

        last_versiton = await self.versions.get_latest(alert.id)

        snapshot = self._build_alert_snapshot(
            alert,
            territories_ids,
        )

        alert_version = AlertVersion(
            alert_id=alert.id,
            alert_version_number=last_versiton.alert_version_number + 1,
            previous_version_id=last_versiton.id,
            changed_by=actor_id,
            change_reason=change_reason,
            snapshot=snapshot,
        )

        await self.versions.add(alert_version)

        return alert

    async def cancel_alert(self, alert_id: UUID, actor_id: UUID, reason: str) -> Alert:
        async with self.session.begin():
            actor = await self.users.get_by_id(actor_id)

            if actor is None:
                raise UserNotFoundError(actor_id)

            can_cancel = self.permissions.has_permission(
                actor.role.name,
                Permission.ALERT_CANCEL,
            )
            can_cancel_any = self.permissions.has_permission(
                actor.role.name,
                Permission.ALERT_CANCEL_ANY,
            )
            if not can_cancel and not can_cancel_any:
                raise PermissionDeniedError()

            alert = await self.repository.get_by_id(alert_id)

            if alert is None:
                raise AlertNotFoundError(alert_id)

            if alert.created_by != actor_id and not can_cancel_any:
                raise PermissionDeniedError()

            canceled_status = await self.statuses.get_by_name("canceled")

            if canceled_status is None:
                raise StatusNotFoundError("canceled")

            alert.current_status_id = canceled_status.id
            alert.current_status = canceled_status
            last_versiton = await self.versions.get_latest(alert.id)
            territories_id = set()

            territories_id_page = await self.territories.get_alert_territories(alert_id)
            for t in territories_id_page.items:
                territories_id.add(t.id)
            current = len(territories_id)

            while territories_id_page.total > current:
                territories_id_page = await self.territories.get_alert_territories(
                    alert_id, Pagination(offset=current)
                )
                for t in territories_id_page.items:
                    territories_id.add(t.id)
                current = len(territories_id)

            snapshot = self._build_alert_snapshot(
                alert,
                territories_id,
            )

            alert_version = AlertVersion(
                alert_id=alert.id,
                alert_version_number=last_versiton.alert_version_number + 1,
                previous_version_id=last_versiton.id,
                changed_by=actor_id,
                change_reason=reason,
                snapshot=snapshot,
            )

            await self.versions.add(alert_version)

            await self.session.flush()
        return alert

    async def publish_alert(self, alert_id: UUID, actor_id: UUID) -> Alert:
        actor = await self.users.get_by_id(actor_id)

        if actor is None:
            raise UserNotFoundError(actor_id)

        can_publish = self.permissions.has_permission(
            actor.role.name,
            Permission.ALERT_PUBLISH,
        )
        if not can_publish:
            raise PermissionDeniedError()

        alert = await self.repository.get_by_id(alert_id)

        if alert is None:
            raise AlertNotFoundError(alert_id)

        published_status = await self.statuses.get_by_name("published")

        if published_status is None:
            raise StatusNotFoundError("published")

        alert.current_status_id = published_status.id
        alert.current_status = published_status
        alert_history_note = AlertStatusHistory(
            alert_id=alert.id,
            status_id=published_status.id,
            reason="approved",
            changed_by=actor_id,
        )

        await self.history.add(alert_history_note)

        await self.session.flush()
        return alert

    async def get_versions(
        self, alert_id: UUID, pagination: Pagination = Pagination
    ) -> Page[AlertVersion]:
        return await self.versions.get_versions(alert_id, pagination)

    async def get_status_history(
        self, alert_id: UUID, pagination: Pagination = Pagination
    ) -> Page[AlertStatusHistory]:
        return await self.history.get_history(alert_id, pagination)


class ProposalService:
    def __init__(
        self,
        repository: IAlertProposalRepository,
    ):
        self.repository = repository

    async def create_proposal(
        self, data: ProposalCreate, actor_id: UUID
    ) -> AlertProposal: ...

    async def get_pending(self) -> list[AlertProposal]: ...

    async def review_proposal(
        self, proposal_id: UUID, data: ProposalReview, actor_id: UUID
    ) -> AlertProposal: ...

    async def convert_to_draft(self, proposal_id: UUID, actor_id: UUID) -> Alert: ...
