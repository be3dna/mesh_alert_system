from enum import StrEnum


class UserState(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"

    @classmethod
    def from_is_active(cls, is_active: bool) -> "UserState":
        return cls.ACTIVE if is_active else cls.INACTIVE
