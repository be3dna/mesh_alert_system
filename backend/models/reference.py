from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.config import DEFAULT_DATETIME_FUNK
from models.base import Base


class ReferenceCategory(Base):
    __tablename__ = "reference_categories"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    articles: Mapped[list["ReferenceArticle"]] = relationship(back_populates="category")


class ReferenceArticle(Base):
    __tablename__ = "reference_articles"

    title: Mapped[str] = mapped_column(String(255), nullable=False)

    content: Mapped[str] = mapped_column(Text, nullable=False)

    category_id: Mapped[UUID] = mapped_column(
        ForeignKey("reference_categories.id"), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    author_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

    editor_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    access_group: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("access_groups.id"), nullable=False
    )

    group: Mapped["AccessGroup"] = relationship(back_populates="references")  # noqa: F821

    category: Mapped["ReferenceCategory"] = relationship(back_populates="articles")

    author: Mapped["User"] = relationship(foreign_keys=[author_id])  # noqa: F821

    editor: Mapped["User"] = relationship(foreign_keys=[editor_id])  # noqa: F821
