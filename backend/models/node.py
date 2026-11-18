from datetime import datetime
from uuid import UUID

from core.config import DEFAULT_DATETIME_FUNK
from sqlalchemy import (
    DOUBLE_PRECISION,
    CheckConstraint,
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class NodeGateway(Base):
    __tablename__ = "node_gateways"

    node_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("nodes.id"), nullable=False
    )
    gateway_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("gateways.id"), nullable=False
    )
    last_seen: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=DEFAULT_DATETIME_FUNK
    )

    UniqueConstraint(node_id, gateway_id)

    node: Mapped["Node"] = relationship(back_populates="gateways")  # H
    gateway: Mapped["Gateway"] = relationship(back_populates="nodes")  # H # noqa: F821


class NodeStatus(Base):
    __tablename__ = "node_statuses"

    name: Mapped[str] = mapped_column(String(30), nullable=False)

    description: Mapped[str] = mapped_column(String(255))

    # REL
    nodes: Mapped[list["Node"]] = relationship(back_populates="status")  # H


class Node(Base):
    __tablename__ = "nodes"
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    latitude: Mapped[float] = mapped_column(DOUBLE_PRECISION)
    longitude: Mapped[float] = mapped_column(DOUBLE_PRECISION)

    territory_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("territories.id")
    )

    status_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("node_statuses.id"), nullable=False
    )

    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=DEFAULT_DATETIME_FUNK
    )

    external_id: Mapped[str] = mapped_column(String(255), nullable=False)

    # REL
    status: Mapped["NodeStatus"] = relationship(back_populates="nodes")  # H
    gateways: Mapped["NodeGateway"] = relationship(back_populates="node")  # H
    deliveries: Mapped[list["AlertDelivery"]] = relationship(back_populates="node")  # noqa: F821 #H

    # CONST
    CheckConstraint("latitude BETWEEN -90 AND 90")
    CheckConstraint("longitude BETWEEN -180 AND 180")
