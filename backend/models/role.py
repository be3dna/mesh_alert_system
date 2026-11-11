

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.config import DEFAULT_DATETIME_FUNK
from models.base import Base
from models.user import User

class RoleHistory(Base):
    __tablename__="role_assignment_history"

    user_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    role_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("roles.id"), nullable=False
    )
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=DEFAULT_DATETIME_FUNK
    )
    assigned_by: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    previous_assignment_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("role_assignment_history.id"), nullable=True
    )

class Role(Base):
    __tablename__="roles"

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        default="user"
    )
    description: Mapped[str] = mapped_column(
        text
    )

    users: Mapped[list["User"]] = relationship(back_populates="role")