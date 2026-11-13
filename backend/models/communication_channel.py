from uuid import UUID
from sqlalchemy import ForeignKey, String, Uuid, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.gateway import Gateway
from models.base import Base


class CommunicationChannel(Base):
    __tablename__ = "communication_channels"

    gateway_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("gateways.id"),
        nullable=False,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    config: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict
    )

    gateway: Mapped["Gateway"] = relationship(
        back_populates="communication_channels"
    )