from datetime import datetime
from uuid import UUID
from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    Enum as SQLEnum,
    Float,
    Integer,
    Null,
)

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


    #REL

    deliveries: Mapped[list["AlertDelivery"]] = relationship(back_populates="status") #H


# Уровень важности оповещения
class AlertSeverity(Base):
    __tablename__ = "alert_severities"
    title: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    alerts: Mapped[list["Alert"]] = relationship(back_populates="severity") #H


# draft, pending, active, completed, cancelled.
class AlertStatus(Base):
    __tablename__ = "alert_statuses"

    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text)

    alerts: Mapped[list["Alert"]] = relationship(back_populates="current_status") #H
    alert_statuses_history: Mapped[list["AlertStatusHistory"]] = relationship(back_populates="status") #H


class AlertType(Base):
    __tablename__ = "alert_types"

    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    alerts: Mapped[list["Alert"]] = relationship(back_populates="alert_type") #H


class ReviewDecision(Base):
    __tablename__ = "review_decisions"
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str | Null] = mapped_column(Text, nullable=True)

    proposals: Mapped[list["AlertProposal"]] = relationship(back_populates="decision") #H


class AlertProposal(Base):
    __tablename__ = "alert_proposals"

    alert_id: Mapped[UUID] = mapped_column(ForeignKey("alerts.id"), nullable=False)

    reviewed_by: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    reviewed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    decision_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("review_decisions.id"), nullable=False
    )

    review_comment: Mapped[str | Null] = mapped_column(Text, nullable=True)

    #REL

    reviewer: Mapped["User | None"] = relationship(
        foreign_keys=[reviewed_by], back_populates="proposals"
    ) #H

    alert: Mapped["Alert | None"] = relationship(back_populates="proposal") #H

    decision: Mapped["ReviewDecision"] = relationship(back_populates="proposals") #H


class AlertDelivery(Base):
    __tablename__ = "alert_deliveries"

    alert_id: Mapped[UUID] = mapped_column(
        ForeignKey("alerts.id"), nullable=False, index=True
    )

    node_id: Mapped[UUID] = mapped_column(
        ForeignKey("nodes.id"), nullable=False, index=True
    )

    status_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("alert_delivery_statuses.id"), nullable=False
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=DEFAULT_DATETIME_FUNK
    )

    acknowledged_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    acknowledgement_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    #REL

    alert: Mapped["Alert"] = relationship("Alert", back_populates="deliveries") #H

    node: Mapped["Node"] = relationship(back_populates="deliveries") #H

    attempts: Mapped[list["DeliveryAttempt"]] = relationship( #H
        "DeliveryAttempt", back_populates="delivery", cascade="all, delete-orphan"
    ) 

    status: Mapped["AlertDeliveryStatus"] = relationship(back_populates="deliveries") #H

    __table_args__ = (
        UniqueConstraint("alert_id", "node_id", name="uq_alert_delivery_node"),
    )


class AlertStatusHistory(Base):
    __tablename__ = "alert_status_history"

    alert_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("alerts.id"), nullable=False
    )
    status_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("alert_statuses.id"), nullable=False
    )
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=DEFAULT_DATETIME_FUNK
    )
    reason: Mapped[str] = mapped_column(Text)
    changed_by: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("users.id"), nullable=False
    )

    #REL
    alert: Mapped["Alert"] = relationship(back_populates="alert_statuses_history") #H
    status: Mapped["AlertStatus"] = relationship( #H
        back_populates="alert_statuses_history"
    ) 
    editor: Mapped["User"] = relationship(back_populates="alert_change_history") #H


class AlertVersion(Base):
    __tablename__ = "alert_versions"

    alert_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("alerts.id"), nullable=False
    )

    alert_version_number: Mapped[int] = mapped_column(Integer, nullable=False)

    previous_version_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("alert_versions.id"), nullable=True
    )

    changed_by: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("users.id"), nullable=False
    )

    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=DEFAULT_DATETIME_FUNK
    )

    change_reason: Mapped[str] = mapped_column(Text, nullable=False)

    snapshot: Mapped[dict] = mapped_column(JSON, nullable=False)

    #REL
    alert: Mapped["Alert"] = relationship(back_populates="versions") #H
    prev_version: Mapped["AlertVersion"] = relationship() #H
    editor: Mapped["User"] = relationship(back_populates="edited_versions") #H


class Alert(Base):
    __tablename__ = "alerts"
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    severity_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("alert_severities.id"), nullable=False
    )
    alert_type_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("alert_types.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=DEFAULT_DATETIME_FUNK
    )
    starts_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=DEFAULT_DATETIME_FUNK
    )
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    created_by: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("users.id"), nullable=False
    )
    current_status_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("alert_statuses.id"), nullable=False
    )
    is_test: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    #CONST
    CheckConstraint("ends_at IS NULL OR ends_at >= starts_at", name="check_alert_dates")

    #REL
    creator: Mapped["User"] = relationship(back_populates="created_alerts") #H
    current_status: Mapped["AlertStatus"] = relationship(back_populates="alerts") #H
    severity: Mapped["AlertSeverity"] = relationship(back_populates="alerts") #H
    alert_type: Mapped["AlertType"] = relationship(back_populates="alerts") #H
    versions: Mapped[list["AlertVersion"]] = relationship(back_populates="alert") #H
    deliveries: Mapped[list["AlertDelivery"]] = relationship(back_populates="alert") #H
    alert_territories: Mapped[list["AlertTerritory"]] = relationship(  # noqa: F821 #H
        back_populates="alert"
    )
    proposal: Mapped["AlertProposal"] = relationship(back_populates="alert") #H
    alert_statuses_history: Mapped[list["AlertStatusHistory"]] = relationship(back_populates="alert") #H
