from datetime import datetime, timezone, UTC
from sqlalchemy import DateTime, ForeignKey
from uuid import UUID, uuid7

from sqlalchemy import TIMESTAMP, Boolean, String, Uuid, false
from sqlalchemy.orm import Mapped, mapped_column
from core.config import DEFAULT_DATETIME_FUNK
from models.base import Base, Role

from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"


    first_name: Mapped[str] = mapped_column(String(50), nullable=False)

    last_name: Mapped[str] = mapped_column(String(50), nullable=False)

    mid_name: Mapped[str] = mapped_column(String(50), nullable=True)

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=DEFAULT_DATETIME_FUNK() 
        #TODO: is UTC best choise? maybe msk?
    )

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_email_verified: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    role_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("roles.id"), nullable=False
    )

    role: Mapped["Role"] = relationship(back_populates="users")
