from datetime import datetime, UTC
from uuid import UUID, uuid7

from sqlalchemy import DateTime, ForeignKey, Uuid, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.alert import AlertDelivery
from models.base import Base


class DeliveryAttempt(Base):
    __tablename__ = "delivery_attempts"

    delivery_id: Mapped[UUID] = mapped_column(
        ForeignKey("alert_deliveries.id"),
        nullable=False,
        index=True
    )

    attempted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC)
    )

    result: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    error_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    delivery: Mapped["AlertDelivery"] = relationship(
        back_populates="attempts"
    )