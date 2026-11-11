from datetime import datetime
from uuid import UUID
from enum import Enum
from sqlalchemy import CheckConstraint, Enum as SQLEnum

from sqlalchemy import DateTime, ForeignKey, String, Text, Uuid, null, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.alert_severity import AlertSeverity
from models.alert_type import AlertType
from models.territory import Territory
from models.user import User
from models.alert_status import AlertStatus
from core.config import DEFAULT_DATETIME_FUNK
from models.base import Base


class Alert(Base):
    __tablename__="alerts"
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    severity_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("alert_severities.id"), nullable=False
    )
    alert_type_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("alert_types.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=DEFAULT_DATETIME_FUNK
    )
    starts_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=DEFAULT_DATETIME_FUNK
    )
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    created_by: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    current_status_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("alert_statuses.id"),
        nullable=False
    )
    territory_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("territories.id"), nullable=False
    )

    CheckConstraint(
        "ends_at IS NULL OR ends_at >= starts_at",
        name="check_alert_dates"
    )

    creator: Mapped["User"] = relationship(back_populates="created_alerts")
    current_status: Mapped["AlertStatus"] = relationship(
        back_populates="alerts"
    )
    territory: Mapped["Territory"] = relationship(
        back_populates="alerts"
    )
    severity: Mapped["AlertSeverity"] = relationship(back_populates="alerts")
    alert_type: Mapped["AlertType"] = relationship(back_populates="alerts")


