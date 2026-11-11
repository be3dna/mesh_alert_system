from datetime import datetime
from uuid import UUID
from enum import Enum
from sqlalchemy import JSON, CheckConstraint, Enum as SQLEnum, Integer

from sqlalchemy import DateTime, ForeignKey, String, Text, Uuid, null, text
from sqlalchemy.orm import Mapped, mapped_column, relationship


from models.territory import Territory
from models.user import User
from core.config import DEFAULT_DATETIME_FUNK
from models.base import Base



class AlertSeverity(Base):
    __tablename__="alert_severity"
    title: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    alerts: Mapped[list["Alert"]] = relationship(back_populates="severity")

class AlertStatusHistory(Base):
    __tablename__="alert_status_history"

    alert_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("alerts.id"),
        nullable=False
    )
    status_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("alert_statuses.id"),
        nullable=False
    )
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=DEFAULT_DATETIME_FUNK
    )
    reason: Mapped[str] = mapped_column(
        Text
    )
    changed_by: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )


    alert: Mapped["Alert"] = relationship(back_populates="alert_statuses_history")
    status: Mapped["AlertStatus"] = relationship(back_populates="alert_statuses_history")
    editor: Mapped["User"] = relationship(back_populates="alert_change_history")

#draft, pending, active, completed, cancelled.
class AlertStatus(Base):
    __tablename__ = "alert_statuses"

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )
    description: Mapped[str] = mapped_column(
        Text
    )

    alerts: Mapped[list["Alert"]] = relationship(
        back_populates="current_status"
    )

class AlertType(Base):
    __tablename__="alert_types"

    name: Mapped[str]=mapped_column(
        String(50),
        nullable=False,
        unique=True
    )

    alerts: Mapped[list["Alert"]] = relationship(back_populates="alert_type")

class AlertVersion(Base):
    __tablename__="alert_versions"

    alert_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("alerts.id"),
        nullable=False
    )

    alert_version_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    previous_version_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("alert_versions.id"),
        nullable=False
    )

    changed_by: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=DEFAULT_DATETIME_FUNK
    )

    change_reason: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    snapshot: Mapped[dict] = mapped_column(
        JSON,
        nullable=False
    )

    alert: Mapped["Alert"] = relationship(back_populates="versions")
    prev_version: Mapped["AlertVersion"] = relationship(back_populates="next_version")
    editor: Mapped["User"] = relationship(back_populates="edited_versions")

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
    territory_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("territories.id"),
        nullable=True
    )

    CheckConstraint(
        "ends_at IS NULL OR ends_at >= starts_at",
        name="check_alert_dates"
    )

    creator: Mapped["User"] = relationship(back_populates="created_alerts")
    current_status: Mapped["AlertStatus"] = relationship(
        back_populates="alerts"
    )
    territory: Mapped["Territory | None"] = relationship(
        back_populates="alerts"
    )
    severity: Mapped["AlertSeverity"] = relationship(back_populates="alerts")
    alert_type: Mapped["AlertType"] = relationship(back_populates="alerts")
    versions: Mapped[list["AlertVersion"]] = relationship(back_populates="alert")


