from datetime import datetime, UTC
from uuid import UUID

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Uuid,
    String,
    Text,
    JSON
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.user import User
from models.base import Base


class SystemEvent(Base):
    __tablename__ = "system_events"

    event_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC)
    )

    source: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    component_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    metadata_: Mapped[dict | None] = mapped_column(
        "metadata",
        JSON,
        nullable=True
    )

    user: Mapped["User | None"] = relationship(
        back_populates="system_events"
    )