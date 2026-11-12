from typing import Any
from uuid import UUID

from sqlalchemy import JSON, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.alert import Alert
from models.base import Base


class AlertTerritory(Base):
    __tablename__ = "alert_territories"

    __table_args__ = (
        UniqueConstraint("alert_id", "territory_id", name="uq_alert_territory"),
    )

    alert_id: Mapped[UUID] = mapped_column(
        ForeignKey("alerts.id"), nullable=False, index=True
    )

    territory_id: Mapped[UUID] = mapped_column(
        ForeignKey("territories.id"), nullable=False, index=True
    )

    alert: Mapped["Alert"] = relationship(back_populates="alert_territories")

    territory: Mapped["Territory"] = relationship(back_populates="alert_territories")


class Territory(Base):
    __tablename__ = "territories"

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    description: Mapped[str] = mapped_column(Text, nullable=False)

    coordinates: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

    alerts: Mapped[list["Alert"]] = relationship(
        back_populates="territory", cascade="all, delete-orphan"
    )
