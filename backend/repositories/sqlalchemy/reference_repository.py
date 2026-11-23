from uuid import UUID

from models.access_group import AccessGroup
from models.reference import ReferenceArticle, ReferenceCategory
from repositories.interfaces.reference import (
    IAccessGroupRepository,
    IReferenceArticleRepository,
    IReferenceCategoryRepository,
)
from repositories.pagination import Page, Pagination
from repositories.sqlalchemy.base import SQLAlchemyNamedRepository, SQLAlchemyRepository
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyReferenceArticleRepository(
    SQLAlchemyRepository[ReferenceArticle], IReferenceArticleRepository
):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ReferenceArticle)

    async def get_by_category(
        self, category_id: UUID, pagination: Pagination = Pagination
    ) -> Page[ReferenceArticle]:
        stmt = (
            select(ReferenceArticle)
            .where(ReferenceArticle.category_id == category_id)
            .order_by(ReferenceArticle.title)
        )
        return await self._paginate(stmt, pagination)

    async def get_by_access_group(
        self, access_group_id: UUID, pagination: Pagination = Pagination
    ) -> Page[ReferenceArticle]:
        stmt = (
            select(ReferenceArticle)
            .where(ReferenceArticle.access_group_id == access_group_id)
            .order_by(ReferenceArticle.title)
        )
        return await self._paginate(stmt, pagination)

    async def get_by_author(
        self, author_id: UUID, pagination: Pagination = Pagination
    ) -> Page[ReferenceArticle]:
        stmt = (
            select(ReferenceArticle)
            .where(ReferenceArticle.author_id == author_id)
            .order_by(ReferenceArticle.title)
        )
        return await self._paginate(stmt, pagination)

    async def get_by_editor(
        self, editor_id: UUID, pagination: Pagination = Pagination
    ) -> Page[ReferenceArticle]:
        stmt = (
            select(ReferenceArticle)
            .where(ReferenceArticle.editor_id == editor_id)
            .order_by(ReferenceArticle.title)
        )
        return await self._paginate(stmt, pagination)


class SQLAlchemyReferenceCategoryRepository(
    SQLAlchemyNamedRepository[ReferenceCategory], IReferenceCategoryRepository
):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ReferenceCategory)


class SQLAlchemyAccessGroupRepository(
    SQLAlchemyRepository[AccessGroup], IAccessGroupRepository
):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_role(
        self, role_id: UUID, pagination: Pagination = Pagination
    ) -> Page[AccessGroup]:
        stmt = (
            select(AccessGroup)
            .where(AccessGroup.role_id == role_id)
            .order_by(AccessGroup.name)
        )
        return await self._paginate(stmt, pagination)
