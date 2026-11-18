from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

T = TypeVar("T")


class IRepository(ABC, Generic[T]):
    @abstractmethod
    async def get_by_id(self, id: UUID) -> T | None: ...

    @abstractmethod
    async def get_all(self, limit: int = 50, offset: int = 0) -> list[T]: ...

    @abstractmethod
    async def add(self, entity: T) -> T: ...

    @abstractmethod
    async def delete(self, id: UUID) -> bool: ...


class INamedRepository(IRepository[T], Generic[T]):
    @abstractmethod
    async def get_by_name(self, name: str) -> T | None: ...
