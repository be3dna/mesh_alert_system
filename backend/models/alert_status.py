from uuid import UUID

from sqlalchemy import String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.alert import Alert
from models.base import Base

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