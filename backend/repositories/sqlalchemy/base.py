from typing import Generic, TypeVar
from uuid import UUID

from models.base import Base
from repositories.interfaces.base import INamedRepository, IRepository
from repositories.pagination import Page, Pagination
from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T", bound=Base)


class SQLAlchemyRepository(IRepository[T], Generic[T]):
    def __init__(
        self,
        session: AsyncSession,
        model: type[T],
    ):
        self.session = session
        self.model = model

    async def _paginate(
        self,
        stmt: Select,
        pagination: Pagination,
    ) -> Page[T]:

        count_stmt = select(func.count()).select_from(
            stmt.order_by(None).limit(None).offset(None).subquery()
        )

        total = (await self.session.execute(count_stmt)).scalar_one()

        paginated_stmt = stmt.limit(pagination.limit).offset(pagination.offset)

        result = await self.session.execute(paginated_stmt)

        return Page(
            items=list(result.scalars().all()),
            total=total,
            limit=pagination.limit,
            offset=pagination.offset,
        )

    async def get_by_id(self, id: UUID) -> T | None:
        return await self.session.get(self.model, id)

    async def get_all(self, pagination: Pagination = Pagination) -> Page[T]:
        stmt = select(self.model).order_by(self.model.id)

        return await self._paginate(stmt, pagination)

    async def add(self, entity: T) -> T:
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def delete(self, id: UUID) -> bool:
        entity = await self.get_by_id(id)

        if entity is None:
            return False

        await self.session.delete(entity)
        await self.session.flush()
        return True


class SQLAlchemyNamedRepository(
    SQLAlchemyRepository[T],
    INamedRepository[T],
    Generic[T],
):
    def __init__(
        self,
        session: AsyncSession,
        model: type[T],
    ):
        super().__init__(session, model)

    async def get_by_name(self, name: str) -> T | None:
        stmt = select(self.model).where(self.model.name == name)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
