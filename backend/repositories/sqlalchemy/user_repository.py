from uuid import UUID

from models.role import Role, RoleHistory
from models.user import User
from repositories.interfaces.users import (
    IRoleHistoryRepository,
    IRoleRepository,
    IUserRepository,
)
from repositories.pagination import Page, Pagination
from repositories.sqlalchemy.base import SQLAlchemyNamedRepository, SQLAlchemyRepository
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyUserRepository(SQLAlchemyRepository[User], IUserRepository):
    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def email_exists(self, email: str) -> bool:
        return await self.get_by_email(email) is not None

    async def get_by_role(
        self, role_id: UUID, pagination: Pagination = Pagination
    ) -> Page[User]:
        stmt = select(User).where(User.role_id == role_id)
        return await self._paginate(stmt, pagination)

    async def count_active_by_role(self, role_id: UUID) -> int:
        stmt = select(func.count()).where(
            User.role_id == role_id, User.is_active == True
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()


class SQLAlchemyRoleRepository(SQLAlchemyNamedRepository[Role], IRoleRepository):
    def __init__(self, session: AsyncSession):
        self.session = session


class SQLAlchemyRoleHistoryRepository(
    SQLAlchemyRepository[RoleHistory], IRoleHistoryRepository
):
    async def get_user_history(
        self, user_id: UUID, pagination: Pagination = Pagination
    ) -> Page[RoleHistory]:
        stmt = (
            select(RoleHistory)
            .where(RoleHistory.user_id == user_id)
            .order_by(desc(RoleHistory.assigned_at))
        )
        return await self._paginate(stmt, pagination)
