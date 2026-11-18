from abc import abstractmethod
from uuid import UUID

from models.access_group import AccessGroup
from models.reference import ReferenceArticle, ReferenceCategory
from repositories.interfaces.base import INamedRepository, IRepository
from repositories.pagination import Page, Pagination


class IReferenceArticleRepository(IRepository[ReferenceArticle]):
    @abstractmethod
    async def get_by_category(
        self, category_id: UUID, pagination: Pagination = Pagination
    ) -> Page[ReferenceArticle]: ...

    @abstractmethod
    async def get_by_access_group(
        self, access_group_id: UUID
    ) -> Page[ReferenceArticle]: ...

    @abstractmethod
    async def get_by_author(
        self, author_id: UUID, pagination: Pagination = Pagination
    ) -> Page[ReferenceArticle]: ...

    @abstractmethod
    async def get_by_editor(
        self, editor_id: UUID, pagination: Pagination = Pagination
    ) -> Page[ReferenceArticle]: ...


class IReferenceCategoryRepository(INamedRepository[ReferenceCategory]): ...


class IAccessGroupRepository(IRepository[AccessGroup]):
    @abstractmethod
    async def get_by_role(
        self, role_id: UUID, pagination: Pagination = Pagination
    ) -> Page[AccessGroup]: ...
