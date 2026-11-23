from pydantic import EmailStr, Field

from .common import Schema


class RegisterRequest(Schema):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    mid_name: str | None = Field(default=None, max_length=50)

class LoginRequest(Schema):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

class PasswordResetRequest(Schema):
    email: EmailStr

class PasswordResetConfirm(Schema):
    token: str
    new_password: str = Field(min_length=8, max_length=128)
