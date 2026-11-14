from uuid import UUID

from geoalchemy2 import Geometry
from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

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

    alert: Mapped["Alert"] = relationship(back_populates="alert_territories")  # noqa: F821

    territory: Mapped["Territory"] = relationship(back_populates="alert_territories")


class Territory(Base):
    __tablename__ = "territories"

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    geom: Mapped[object] = mapped_column(
        Geometry(geometry_type="MULTIPOLYGON", srid=4326, spatial_index=True),
        nullable=False,
    )
    alert_territories: Mapped[list["AlertTerritory"]] = relationship(
        "AlertTerritory", back_populates="territory"
    )
