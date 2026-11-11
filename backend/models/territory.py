from typing import Any

from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.alert import Alert
from models.base import Base


class Territory(Base):
    __tablename__="territories"

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    coordinates: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        nullable=False
    )
    
    alerts: Mapped[list["Alert"]] = relationship(
        back_populates="territory",
        cascade="all, delete-orphan"
    )