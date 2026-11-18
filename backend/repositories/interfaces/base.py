from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from repositories.pagination import Page, Pagination

T = TypeVar("T")


class IRepository(ABC, Generic[T]):
    @abstractmethod
    async def get_by_id(self, id: UUID) -> T | None: ...

    @abstractmethod
    async def get_all(self, pagination: Pagination = Pagination) -> Page[T]: ...

    @abstractmethod
    async def add(self, entity: T) -> T: ...

    @abstractmethod
    async def delete(self, id: UUID) -> bool: ...


class INamedRepository(IRepository[T], Generic[T]):
    @abstractmethod
    async def get_by_name(self, name: str) -> T | None: ...
