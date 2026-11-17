from datetime import datetime
from sqlalchemy import DateTime, ForeignKey
from uuid import UUID
from sqlalchemy import TIMESTAMP, Boolean, String, Uuid, false
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from core.config import DEFAULT_DATETIME_FUNK
from models.base import Base


class User(Base):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    mid_name: Mapped[str] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=DEFAULT_DATETIME_FUNK
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

    #REL
    role: Mapped["Role"] = relationship(back_populates="users") #H  # noqa: F821
    created_alerts: Mapped[list["Alert"]] = relationship(back_populates="creator")  # noqa: F821 #H
    alert_change_history: Mapped[list["AlertStatusHistory"]] = relationship(  # noqa: F821 #H
        back_populates="editor"
    )
    edited_versions: Mapped[list["AlertVersion"]] = relationship(  # noqa: F821 #H
        back_populates="editor"
    )
    role_history: Mapped[list["RoleHistory"]] = relationship(  #H # noqa: F821
        back_populates="user", foreign_keys="RoleHistory.user_id"
    ) 
    role_changer_history: Mapped[list["RoleHistory"]] = relationship( #H # noqa: F821
        back_populates="changer", foreign_keys="RoleHistory.assigned_by"
    )  
    proposals: Mapped[list["AlertProposal"]] = relationship(back_populates="reviewer")  # noqa: F821 #H
    system_events: Mapped[list["SystemEvent"]] = relationship(back_populates="user") #H  # noqa: F821
