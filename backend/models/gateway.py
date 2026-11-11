
from typing import Any
from uuid import UUID

from sqlalchemy import JSON, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import Base

class GatewayStatus(Base):
    __tablename__="gateway_statuses"

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text
    )

    gateways: Mapped["Gateway"] = relationship(back_populates="gateways.id")

class GatewayType(Base):
    __tablename__="gateway_types"

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text
    )

    gateways: Mapped[list["Gateway"]] = relationship(back_populates="gateway_type")

class Gateway(Base):
    __tablename__="gateways"

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    status_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("gateway_statuses.id"),
        nullable=False
    )

    type_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("gateway_types.id"),
        nullable=False
    )

    conf: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        nullable=False
    )
        
    status: Mapped["GatewayStatus"] = relationship(back_populates="gateways")
    gateway_type: Mapped["GatewayType"] = relationship(back_populates="gateways")


