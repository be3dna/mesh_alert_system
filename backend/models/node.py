
from datetime import datetime
from uuid import UUID

from sqlalchemy import DOUBLE_PRECISION, CheckConstraint, Date, DateTime, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.config import DEFAULT_DATETIME_FUNK
from backend.models.base import Base

class NodeStatus(Base):
    __tablename__="node_statuses"

    name: Mapped[str]=mapped_column(
        String(30),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(255)
    )

    nodes: Mapped[list["Node"]] = relationship(back_populates="status")

class Node(Base):
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    latitude: Mapped[float] = mapped_column(DOUBLE_PRECISION)
    longitude: Mapped[float] = mapped_column(DOUBLE_PRECISION)

    territory_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("territories.id")
    )
    
    status_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("node_statuses.id"),
        nullable=False
    )

    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=DEFAULT_DATETIME_FUNK
    )

    external_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    status: Mapped["NodeStatus"] = relationship(back_populates="node_statuses.id")

    CheckConstraint("latitude BETWEEN -90 AND 90")
    CheckConstraint("longitude BETWEEN -180 AND 180")
