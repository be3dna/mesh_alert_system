from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.alert import Alert
from backend.models.base import Base


class AlertSeverity(Base):
    __tablename__="alert_severity"
    title: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    alerts: Mapped[list["Alert"]] = relationship(back_populates="severity")
    