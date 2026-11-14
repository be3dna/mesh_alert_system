from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, Text, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.config import DEFAULT_DATETIME_FUNK
from models.base import Base


class RoleHistory(Base):
    __tablename__ = "role_assignment_history"

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

    user: Mapped["User"] = relationship("User", back_populates="role_history")  # noqa: F821
    role: Mapped["Role"] = relationship(back_populates="user_history")
    changer: Mapped["User"] = relationship("User", back_populates="role_changer_history")  # noqa: F821


class Role(Base):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, default="user"
    )
    description: Mapped[str] = mapped_column(Text)

    users: Mapped[list["User"]] = relationship("User", back_populates="role")  # noqa: F821
    user_history: Mapped[list["RoleHistory"]] = relationship(back_populates="role")
