from uuid import UUID

from core.exceptions import PermissionDeniedError, RoleNotFoundError, UserNotFoundError
from models.role import Role, RoleHistory
from models.user import User
from repositories.interfaces.users import IRoleHistoryRepository, IRoleRepository
from repositories.pagination import Page, Pagination
from services.permissions import ROLE_PERMISSIONS, Permission
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class RoleService:
    def __init__(
        self,
        repository: IRoleRepository,
        history: IRoleHistoryRepository,
        session: AsyncSession,
    ):
        self.repository = repository
        self.history = history
        self.session = session

    async def assign_role(self, user_id: UUID, role_id: UUID, actor_id: UUID) -> None:
        async with self.session.begin():
            result = await self.session.scalars(
                select(User)
                .where(User.id.in_({user_id, actor_id}))
                .order_by(User.id)
                .with_for_update()
                .execution_options(populate_existing=True)
            )
            users = {user.id: user for user in result}
            for required_id in (actor_id, user_id):
                if required_id not in users:
                    raise UserNotFoundError(required_id)

            actor, user = users[actor_id], users[user_id]
            permissions = await self._permissions_for(actor)
            if Permission.USERS_MANAGE_ROLES not in permissions:
                if Permission.OPERATOR_MANAGE_ROLE not in permissions:
                    raise PermissionDeniedError("Permission required to assign roles")
                current = await self._get_role(user.role_id)
                requested = await self._get_role(role_id)
                if {current.name, requested.name} - {"user", "operator"}:
                    raise PermissionDeniedError("Role assignment is limited to users and operators")
            else:
                await self._get_role(role_id)

            if user.role_id == role_id:
                return

            latest = await self.history.get_user_history(user_id, Pagination(limit=1))
            previous_id = latest.items[0].id if latest.items else None
            user.role_id = role_id
            await self.history.add(
                RoleHistory(
                    user_id=user_id,
                    role_id=role_id,
                    assigned_by=actor_id,
                    previous_assignment_id=previous_id,
                )
            )

    async def get_user_role(self, user_id: UUID) -> Role:
        async with self.session.begin():
            user = await self._get_user(user_id)
            return await self._get_role(user.role_id)

    async def get_role_history(
        self, user_id: UUID, pagination: Pagination | None = None
    ) -> Page[RoleHistory]:
        async with self.session.begin():
            await self._get_user(user_id)
            return await self.history.get_user_history(user_id, pagination or Pagination())

    async def check_permission(self, actor_id: UUID, permission: str) -> bool:
        async with self.session.begin():
            actor = await self._get_user(actor_id)
            return permission in await self._permissions_for(actor)

    async def ensure_permission(self, actor_id: UUID, permission: str) -> None:
        if not await self.check_permission(actor_id, permission):
            raise PermissionDeniedError(f"Permission required: {permission}")

    async def _get_user(self, user_id: UUID) -> User:
        user = await self.session.get(User, user_id, populate_existing=True)
        if user is None:
            raise UserNotFoundError(user_id)
        return user

    async def _get_role(self, role_id: UUID) -> Role:
        role = await self.repository.get_by_id(role_id)
        if role is None:
            raise RoleNotFoundError(role_id)
        return role

    async def _permissions_for(self, user: User) -> frozenset[Permission]:
        if not user.is_active:
            return frozenset()
        role = await self._get_role(user.role_id)
        return ROLE_PERMISSIONS.get(role.name, frozenset())
