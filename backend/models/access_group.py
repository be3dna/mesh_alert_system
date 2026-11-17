from enum import UNIQUE
from uuid import UUID

from sqlalchemy import ForeignKey, String, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class AccessGroupRole(Base):
    __tablename__ = "access_group_roles"
    access_group_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("access_groups.id"), nullable=False
    )
    role_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("roles.id"), nullable=False)

    UniqueConstraint(access_group_id, role_id)

    group: Mapped["AccessGroup"] = relationship(back_populates="roles") #H
    role: Mapped["Role"] = relationship(back_populates="groups")  # noqa: F821 #H


class AccessGroup(Base):
    __tablename__ = "access_groups"
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    roles: Mapped[list["AccessGroupRole"]] = relationship(back_populates="group") #H
    references: Mapped[list["ReferenceArticle"]] = relationship(back_populates="group")  # noqa: F821 #H
