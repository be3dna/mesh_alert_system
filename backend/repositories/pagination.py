from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Pagination:
    limit: int = 50
    offset: int = 0

    def __post_init__(self):
        if not 1 <= self.limit <= 100:
            raise ValueError("limit must be between 1 and 100")
        if self.offset < 0:
            raise ValueError("offset must be non-negative")


@dataclass
class Page(Generic[T]):
    items: list[T]
    total: int
    limit: int
    offset: int