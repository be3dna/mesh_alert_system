from abc import abstractmethod
from uuid import UUID

from models.role import Role, RoleHistory
from models.user import User
from repositories.interfaces.base import IRepository
from repositories.pagination import Page, Pagination


class IUserRepository(IRepository[User]):
    @abstractmethod
    async def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def email_exists(self, email: str) -> bool: ...

    @abstractmethod
    async def get_by_role(
        self, role_id: UUID, pagination: Pagination = Pagination
    ) -> Page[User]: ...

    @abstractmethod
    async def count_active_by_role(self, role_id: UUID) -> int: ...


class IRoleRepository(IRepository[Role]):
    @abstractmethod
    async def get_by_name(self, name: str) -> Role | None: ...


class IRoleHistoryRepository(IRepository[RoleHistory]):
    @abstractmethod
    async def get_user_history(
        self, user_id: UUID, pagination: Pagination = Pagination
    ) -> Page[RoleHistory]: ...
