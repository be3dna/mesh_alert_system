from abc import abstractmethod
from uuid import UUID

from backend.models.access_group import AccessGroup
from backend.models.reference import ReferenceArticle, ReferenceCategory
from backend.repositories.interfaces.base import INamedRepository, IRepository


class IReferenceArticleRepository(IRepository[ReferenceArticle]):
    @abstractmethod
    async def get_by_category(self, category_id: UUID) -> list[ReferenceArticle]: ...

    @abstractmethod
    async def get_by_access_group(
        self, access_group_id: UUID
    ) -> list[ReferenceArticle]: ...

    @abstractmethod
    async def get_by_author(self, author_id: UUID) -> list[ReferenceArticle]: ...

    @abstractmethod
    async def get_by_editor(self, editor_id: UUID) -> list[ReferenceArticle]: ...


class IReferenceCategoryRepository(INamedRepository[ReferenceCategory]): ...


class IAccessGroupRepository(IRepository[AccessGroup]):
    @abstractmethod
    async def get_by_role(self, role_id: UUID) -> list[AccessGroup]: ...
