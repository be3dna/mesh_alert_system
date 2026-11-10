from datetime import UTC, datetime
from uuid import UUID, uuid7

from sqlalchemy import DateTime, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from core.config import DEFAULT_DATETIME_FUNK
from models.base import Base

class RoleHistory(Base):
    __tablename__="role_assignment_history"

    user_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    role_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("roles.id"), nullable=False
    )
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=DEFAULT_DATETIME_FUNK()
    )
    assigned_by: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    previous_assignment_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("role_assignment_history.id"), nullable=True
    )
