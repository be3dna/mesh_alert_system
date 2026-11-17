from datetime import datetime
from uuid import UUID
from pydantic import EmailStr, Field
from .common import Schema, UUIDRead

class UserUpdate(Schema):
    first_name: str | None = Field(default=None, min_length=1, max_length=50)
    last_name: str | None = Field(default=None, min_length=1, max_length=50)
    mid_name: str | None = Field(default=None, max_length=50)

class UserRead(UUIDRead):
    email: EmailStr
    first_name: str
    last_name: str
    mid_name: str | None
    role_id: UUID
    is_active: bool
    is_email_verified: bool
    created_at: datetime
    last_login_at: datetime | None

class UserPublic(UUIDRead):
    first_name: str
    last_name: str

class UserAdminUpdate(Schema):
    is_active: bool | None = None
    role_id: UUID | None = None
