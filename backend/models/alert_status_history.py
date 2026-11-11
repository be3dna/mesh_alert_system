

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.config import DEFAULT_DATETIME_FUNK
from backend.models.alert import Alert
from backend.models.alert_status import AlertStatus
from backend.models.base import Base
from backend.models.user import User


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