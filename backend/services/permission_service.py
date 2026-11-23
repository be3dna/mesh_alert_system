from collections.abc import Iterable

from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.exceptions import PermissionDeniedError, UserNotFoundError
from backend.repositories.interfaces.users import IUserRepository
from backend.services.permissions import ROLE_PERMISSIONS, Permission


class PermissionService:
    def __init__(self, users: IUserRepository, session: AsyncSession):
        self.users = users
        self.session = session

    def has_permission(
        self,
        role_name: str,
        permission: Permission,
    ) -> bool:
        permissions = ROLE_PERMISSIONS.get(role_name, frozenset())

        return permission in permissions

    def require_permission(
        self,
        role_name: str,
        permission: Permission,
    ) -> None:
        if not self.has_permission(role_name, permission):
            raise PermissionDeniedError(f"Permission required: {permission}")

    async def user_permissions_check(self, actor_id, permissions: Iterable[Permission]):
        actor = await self.users.get_by_id(actor_id)

        if actor is None:
            raise UserNotFoundError(actor_id)

        await self.session.refresh(actor.role)

        for permission in permissions:
            if self.has_permission(
                actor.role.name,
                permission,
            ):
                return True

        return False
