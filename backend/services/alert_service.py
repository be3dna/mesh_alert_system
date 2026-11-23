from datetime import datetime
from uuid import UUID

from backend.state.proposal_status import ProposalStatus
from core.exceptions import (
    AlertNotFoundError,
    AlreadyReviewedError,
    InvalidAlertStatusError,
    InvalidTerritoryError,
    StatusNotFoundError,
    TimeMachineError,
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
from backend.services.permission_service import PermissionDeniedError, PermissionService
from backend.services.permissions import Permission
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from state.alert_state_machine import AlertStateMachine
from state.alert_status import AlertStatus


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
            if not await self.permissions.user_permissions_check(
                actor_id, [Permission.ALERT_CREATE]
            ):
                raise PermissionDeniedError()

            requires_review = not await self.permissions.user_permissions_check(
                actor_id, [Permission.ALERT_PROPOSE]
            )

            status_name = AlertStateMachine.initial_status(
                requires_review=requires_review
            )
            status = await self.statuses.get_by_name(status_name)
            if status is None:
                raise StatusNotFoundError(status_name)

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
        self, filters: AlertFilters, pagination: Pagination | None = None
    ) -> Page[Alert]:
        pagination = pagination or Pagination()
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
        actor_id: UUID,
    ):
        if not await self.permissions.user_permissions_check(
            actor_id, [Permission.ALERT_UPDATE, Permission.ALERT_UPDATE_ANY]
        ):
            raise PermissionDeniedError()

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
        self,
        alert_id: UUID,
        data: AlertUpdate,
        actor_id: UUID,
    ) -> Alert:
        async with self.session.begin():
            if not await self.permissions.user_permissions_check(
                actor_id, [Permission.ALERT_UPDATE, Permission.ALERT_UPDATE_ANY]
            ):
                raise PermissionDeniedError()

            alert = await self.repository.get_by_id(alert_id)

            if alert is None:
                raise AlertNotFoundError(alert_id)

            if (
                alert.created_by != actor_id
                and not await self.permissions.user_permissions_check(
                    Permission.ALERT_UPDATE_ANY
                )
            ):
                raise PermissionDeniedError()

            update_data = data.model_dump(exclude_unset=True)

            territory_ids = update_data.pop("territories_id", None)
            change_reason = update_data.pop("change_reason", None)

            # Изменяем обычные поля
            for field, value in update_data.items():
                setattr(alert, field, value)

            # Обновляем территории, только если они переданы
            if territory_ids is not None:
                territory_ids = list(set(territory_ids))

                territories = await self.territories.get_by_ids(territory_ids)

                if len(territories) != len(territory_ids):
                    raise InvalidTerritoryError()

                await self.update_territories(
                    alert_id,
                    territory_ids,
                )

            else:
                # Получаем существующие территории
                territory_ids = [
                    item.territory_id
                    for item in (
                        await self.session.scalars(
                            select(AlertTerritory).where(
                                AlertTerritory.alert_id == alert_id
                            )
                        )
                    ).all()
                ]

            await self.session.flush()

            last_version = await self.versions.get_latest(alert.id)

            snapshot = self._build_alert_snapshot(
                alert,
                territory_ids,
            )

            alert_version = AlertVersion(
                alert_id=alert.id,
                alert_version_number=last_version.alert_version_number + 1,
                previous_version_id=last_version.id,
                changed_by=actor_id,
                change_reason=change_reason,
                snapshot=snapshot,
            )

            await self.versions.add(alert_version)

        return alert

    async def cancel_alert(self, alert_id: UUID, actor_id: UUID, reason: str) -> Alert:
        async with self.session.begin():
            if not await self.permissions.user_permissions_check(
                actor_id, [Permission.ALERT_CANCEL, Permission.ALERT_CANCEL_ANY]
            ):
                raise PermissionDeniedError()

            alert = await self.repository.get_by_id(alert_id)

            if alert is None:
                raise AlertNotFoundError(alert_id)

            if (
                alert.created_by != actor_id
                and not await self.permissions.user_permissions_check(
                    actor_id, [Permission.ALERT_CANCEL_ANY]
                )
            ):
                raise PermissionDeniedError()

            await self._change_status(alert, AlertStatus.CANCELED, actor_id, reason)
        return alert

    async def publish_alert(self, alert_id: UUID, actor_id: UUID) -> Alert:
        async with self.session.begin():
            if not await self.permissions.user_permissions_check(
                actor_id, [Permission.ALERT_PUBLISH]
            ):
                raise PermissionDeniedError()

            alert = await self.repository.get_by_id(alert_id)

            if alert is None:
                raise AlertNotFoundError(alert_id)

            await self._change_status(
                alert, AlertStatus.PUBLISHED, actor_id, "publication"
            )
        return alert

    async def _change_status(
        self, alert: Alert, target: AlertStatus, actor_id: UUID, reason: str
    ) -> None:
        await self.session.refresh(
            alert, ["current_status_id", "current_status"], with_for_update=True
        )
        current = alert.current_status.name
        if current == target == AlertStatus.CANCELED:
            return
        if not AlertStateMachine.can_transition(current, target):
            raise InvalidAlertStatusError(
                f"cannot transition from {current} to {target}"
            )

        status = await self.statuses.get_by_name(target)
        if status is None:
            raise StatusNotFoundError(target)

        alert.current_status_id = status.id
        alert.current_status = status
        await self.history.add(
            AlertStatusHistory(
                alert_id=alert.id,
                status_id=status.id,
                reason=reason,
                changed_by=actor_id,
            )
        )
        await self.session.flush()

    async def get_versions(
        self, alert_id: UUID, pagination: Pagination | None = None
    ) -> Page[AlertVersion]:
        pagination = pagination or Pagination()
        return await self.versions.get_versions(alert_id, pagination)

    async def get_status_history(
        self, alert_id: UUID, pagination: Pagination | None = None
    ) -> Page[AlertStatusHistory]:
        pagination = pagination or Pagination()
        return await self.history.get_history(alert_id, pagination)


class ProposalService:
    def __init__(
        self,
        repository: IAlertProposalRepository,
        session: AsyncSession,
        permissions: PermissionService,
    ):
        self.repository = repository
        self.session = session
        self.permissions = permissions

    async def create_proposal(
        self, data: ProposalCreate, actor_id: UUID
    ) -> AlertProposal:
        if not await self.permissions.user_permissions_check(
            actor_id, [Permission.ALERT_PROPOSE]
        ):
            raise PermissionDeniedError()

        proposal = AlertProposal(
            alert_id=data.alert_id,
            decision_id=data.decision_id,
            reviewed_by=actor_id,
            reviewed_at=data.reviewed_at,
            review_comment=data.review_comment,
        )
        await self.proposals.add(proposal)

    async def get_pending(
        self, actor_id: UUID, pagination: Pagination | None = None
    ) -> Page[AlertProposal]:
        if not await self.permissions.user_permissions_check(
            actor_id, [Permission.ALERT_REVIEW]
        ):
            raise PermissionDeniedError()

        pagination = pagination or Pagination()

        return await self.repository.get_pending(pagination)

    async def review_proposal(
        self, proposal_id: UUID, data: ProposalReview, actor_id: UUID
    ) -> AlertProposal:
        async with self.session.begin():
            if not await self.permissions.user_permissions_check(
                actor_id, [Permission.ALERT_REVIEW]
            ):
                raise PermissionDeniedError()

            proposal = await self.repository.get_by_id(proposal_id)
            await self.session.flush(proposal.decision)

            if (
                proposal.decision.name == ProposalStatus.APPROVED
                or proposal.decision.name == ProposalStatus.REJECTED
            ):
                raise AlreadyReviewedError(proposal_id)

            if data.reviewed_at > datetime.now():
                raise TimeMachineError()
                
            update_data = data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(proposal, field, value)

            await self.session.flash()
        return proposal
