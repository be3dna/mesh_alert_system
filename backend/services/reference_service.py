from datetime import UTC, datetime
from uuid import UUID

from core.exceptions import (
    ReferenceArticleNotFoundError,
    ReferenceCategoryNotFoundError,
)
from models.reference import ReferenceArticle
from repositories.interfaces.reference import (
    IReferenceArticleRepository,
    IReferenceCategoryRepository,
)
from repositories.pagination import Page, Pagination
from schemas.references import ReferenceArticleCreate, ReferenceArticleUpdate
from sqlalchemy.ext.asyncio import AsyncSession


class ReferenceService:
    def __init__(
        self,
        repository: IReferenceArticleRepository,
        cotegories: IReferenceCategoryRepository,
        session: AsyncSession,
    ):
        self.repository = repository
        self.categories = cotegories
        self.session = session

    async def get_articles(
        self, pagination: Pagination | None = None
    ) -> Page[ReferenceArticle]:
        async with self.session.begin():
            return await self.repository.get_all(pagination or Pagination())

    async def get_article(self, article_id: UUID) -> ReferenceArticle | None:
        async with self.session.begin():
            return await self.repository.get_by_id(article_id)

    async def create_article(
        self, data: ReferenceArticleCreate, actor_id: UUID
    ) -> ReferenceArticle:
        async with self.session.begin():
            await self._require_category(data.category_id)
            article = await self.repository.add(
                ReferenceArticle(**data.model_dump(), author_id=actor_id)
            )
        return article

    async def update_article(
        self, article_id: UUID, data: ReferenceArticleUpdate, actor_id: UUID
    ) -> ReferenceArticle:
        async with self.session.begin():
            article = await self.repository.get_by_id(article_id)
            if article is None:
                raise ReferenceArticleNotFoundError(article_id)

            changes = {
                field: value
                for field, value in data.model_dump(exclude_unset=True, exclude_none=True).items()
                if getattr(article, field) != value
            }
            if not changes:
                return article

            if "category_id" in changes:
                await self._require_category(changes["category_id"])

            for field, value in changes.items():
                setattr(article, field, value)
            article.editor_id = actor_id
            article.updated_at = datetime.now(UTC)
        return article

    async def _require_category(self, category_id: UUID) -> None:
        if await self.categories.get_by_id(category_id) is None:
            raise ReferenceCategoryNotFoundError(category_id)
