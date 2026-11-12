from datetime import datetime, UTC
from uuid import UUID, uuid7

from sqlalchemy import DateTime, ForeignKey, Uuid, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.config import DEFAULT_DATETIME_FUNK
from backend.models.user import User
from models.base import Base


class ReferenceArticle(Base):
    __tablename__ = "reference_articles"

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=DEFAULT_DATETIME_FUNK
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=DEFAULT_DATETIME_FUNK,
        onupdate=DEFAULT_DATETIME_FUNK
    )

    author_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    editor_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    access_group: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    author: Mapped["User"] = relationship(
        foreign_keys=[author_id],
        back_populates="authored_articles"
    )

    editor: Mapped["User | None"] = relationship(
        foreign_keys=[editor_id],
        back_populates="edited_articles"
    )