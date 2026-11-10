

from uuid import UUID, uuid7

from sqlalchemy import String, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.user import User


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