
from typing import Any
from uuid import UUID

from sqlalchemy import JSON, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

class GatewayStatus(Base):
    __tablename__="gateway_statuses"

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text
    )

    gateways: Mapped[list["Gateway"]] = relationship(back_populates="status") #H

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

    #REL
    gateways: Mapped[list["Gateway"]] = relationship(back_populates="gateway_type") #H

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

    #REL
    communication_channels: Mapped[list["CommunicationChannel"]] = relationship(back_populates="gateway") #H  # noqa: F821
    status: Mapped["GatewayStatus"] = relationship(back_populates="gateways") #H
    gateway_type: Mapped["GatewayType"] = relationship(back_populates="gateways") #H
    nodes: Mapped["NodeGateway"] = relationship(back_populates="gateway")  #H # noqa: F821


