from uuid import UUID

from sqlalchemy import ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class AccessGroupRole(Base):
    __tablename__ = "access_group_roles"
    access_group_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("access_groups.id"), nullable=False
    )
    role_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("roles.id"), nullable=False)

    group: Mapped["AccessGroup"] = relationship(back_populates="roles")
    role: Mapped["Role"] = relationship(back_populates="groups")  # noqa: F821


class AccessGroup(Base):
    __tablename__ = "access_groups"
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    describtion: Mapped[str | None] = mapped_column(Text, nullable=True)

    roles: Mapped[list["AccessGroupRole"]] = relationship(back_populates="group")
    references: Mapped[list["ReferenceArticle"]] = relationship(back_populates="group")  # noqa: F821
