

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.alert import Alert
from backend.models.base import Base


class AlertType(Base):
    __tablename__="alert_types"

    name: Mapped[str]=mapped_column(
        String(50),
        nullable=False,
        unique=True
    )

    alerts: Mapped[list["Alert"]] = relationship(back_populates="alert_type")