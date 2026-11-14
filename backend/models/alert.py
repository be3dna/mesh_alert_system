from datetime import UTC, datetime
from uuid import UUID
from sqlalchemy import JSON, CheckConstraint, Enum as SQLEnum, Float, Integer

from sqlalchemy import DateTime, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UniqueConstraint


from models.delivery_attempt import DeliveryAttempt
from models.node import Node
from models.user import User
from core.config import DEFAULT_DATETIME_FUNK
from models.base import Base


# Отправка, Ошибка, Повторная отправка, Доставлено
class AlertDeliveryStatus(Base):
    __tablename__ = "alert_delivery_statuses"

    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    description: Mapped[str] = mapped_column(Text)

    deliveries: Mapped[list["AlertDelivery"]] = relationship(back_populates="status")


# Уровень важности оповещения
class AlertSeverity(Base):
    __tablename__ = "alert_severities"
    title: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    alerts: Mapped[list["Alert"]] = relationship(back_populates="severity")


# draft, pending, active, completed, cancelled.
class AlertStatus(Base):
    __tablename__ = "alert_statuses"

    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text)

    alerts: Mapped[list["Alert"]] = relationship(back_populates="current_status")


class AlertType(Base):
    __tablename__ = "alert_types"

    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    alerts: Mapped[list["Alert"]] = relationship(back_populates="alert_type")


class AlertProposal(Base):
    __tablename__ = "alert_proposals"

    proposed_by: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)

    description: Mapped[str] = mapped_column(Text, nullable=False)

    proposed_severity: Mapped[str] = mapped_column(String(30), nullable=False)

    latitude: Mapped[float] = mapped_column(Float, nullable=False)

    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    radius_meters: Mapped[int] = mapped_column(Integer, nullable=False)

    type: Mapped[str] = mapped_column(String(50), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC)
    )

    starts_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    ends_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    reviewed_by: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    reviewed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    decision: Mapped[str] = mapped_column(String(30), nullable=False, default="pending")

    created_alert_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("alerts.id"), nullable=True
    )

    proposer: Mapped["User"] = relationship(
        foreign_keys=[proposed_by], back_populates="proposed_alerts"
    )

    reviewer: Mapped["User | None"] = relationship(
        foreign_keys=[reviewed_by], back_populates="reviewed_proposals"
    )

    created_alert: Mapped["Alert | None"] = relationship(
        back_populates="source_proposal"
    )


class AlertDelivery(Base):
    __tablename__ = "alert_deliveries"

    alert_id: Mapped[UUID] = mapped_column(
        ForeignKey("alerts.id"), nullable=False, index=True
    )

    node_id: Mapped[UUID] = mapped_column(
        ForeignKey("nodes.id"), nullable=False, index=True
    )

    status_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("alert_delivery_statuses.id"), nullable=False
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=DEFAULT_DATETIME_FUNK
    )

    acknowledged_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    acknowledgement_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    alert: Mapped["Alert"] = relationship("Alert", back_populates="deliveries")

    node: Mapped["Node"] = relationship(back_populates="deliveries")

    attempts: Mapped[list["DeliveryAttempt"]] = relationship(
        "DeliveryAttempt", back_populates="delivery", cascade="all, delete-orphan"
    )

    status: Mapped["AlertDeliveryStatus"] = relationship(back_populates="deliveries")

    __table_args__ = (
        UniqueConstraint("alert_id", "node_id", name="uq_alert_delivery_node"),
    )


class AlertStatusHistory(Base):
    __tablename__ = "alert_status_history"

    alert_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("alerts.id"), nullable=False
    )
    status_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("alert_statuses.id"), nullable=False
    )
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=DEFAULT_DATETIME_FUNK
    )
    reason: Mapped[str] = mapped_column(Text)
    changed_by: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False
    )

    alert: Mapped["Alert"] = relationship(back_populates="alert_statuses_history")
    status: Mapped["AlertStatus"] = relationship(
        back_populates="alert_statuses_history"
    )
    editor: Mapped["User"] = relationship(back_populates="alert_change_history")


class AlertVersion(Base):
    __tablename__ = "alert_versions"

    alert_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("alerts.id"), nullable=False
    )

    alert_version_number: Mapped[int] = mapped_column(Integer, nullable=False)

    previous_version_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("alert_versions.id"), nullable=True
    )

    changed_by: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False
    )

    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=DEFAULT_DATETIME_FUNK
    )

    change_reason: Mapped[str] = mapped_column(Text, nullable=False)

    snapshot: Mapped[dict] = mapped_column(JSON, nullable=False)

    alert: Mapped["Alert"] = relationship(back_populates="versions")
    prev_version: Mapped["AlertVersion"] = relationship(back_populates="next_version")
    editor: Mapped["User"] = relationship(back_populates="edited_versions")


class Alert(Base):
    __tablename__ = "alerts"
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
        Uuid(as_uuid=True), ForeignKey("alert_statuses.id"), nullable=False
    )

    CheckConstraint("ends_at IS NULL OR ends_at >= starts_at", name="check_alert_dates")

    creator: Mapped["User"] = relationship(back_populates="created_alerts")
    current_status: Mapped["AlertStatus"] = relationship(back_populates="alerts")
    severity: Mapped["AlertSeverity"] = relationship(back_populates="alerts")
    alert_type: Mapped["AlertType"] = relationship(back_populates="alerts")
    versions: Mapped[list["AlertVersion"]] = relationship(back_populates="alert")
    deliveries: Mapped[list["AlertDelivery"]] = relationship(
        "AlertDelivery", back_populates="alert"
    )
    alert_territories: Mapped[list["AlertTerritory"]] = relationship(  # noqa: F821
        "AlertTerritory", back_populates="alert"
    )
