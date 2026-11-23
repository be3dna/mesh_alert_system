import hashlib
import hmac
import secrets
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from uuid import UUID

from core.exceptions import AppError, RoleNotFoundError
from models.auth_session import AuthSession
from models.role import Role
from models.user import User
from repositories.interfaces.users import IRoleRepository, IUserRepository
from schemas.auth import RegisterRequest
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.concurrency import run_in_threadpool


class InvalidCredentialsError(AppError):
    pass


class EmailAlreadyRegisteredError(AppError):
    pass


@dataclass(frozen=True)
class AuthContext:
    user_id: UUID
    role: str


def _token_hash(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def _derive_password(password: str, salt: bytes) -> str:
    return hashlib.scrypt(
        password.encode(), salt=salt, n=2**17, r=8, p=1,
        maxmem=256 * 1024 * 1024, dklen=32,
    ).hex()


def _hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    return f"scrypt${salt.hex()}${_derive_password(password, salt)}"


def _verify_password(password: str, stored: str | None) -> bool:
    parts = (stored or "").split("$")
    scheme, salt_hex, expected = parts if len(parts) == 3 else ("", "", "")
    try:
        salt = bytes.fromhex(salt_hex)
    except ValueError:
        salt = b""
    valid_format = scheme == "scrypt" and len(salt) == 16 and len(expected) == 64
    actual = _derive_password(password, salt if valid_format else bytes(16))
    return valid_format and hmac.compare_digest(actual, expected)


class AuthService:
    def __init__(
        self, session: AsyncSession, users: IUserRepository, roles: IRoleRepository,
        session_lifetime: timedelta,
    ):
        self.session = session
        self.users = users
        self.roles = roles
        self.session_lifetime = session_lifetime

    async def register(self, data: RegisterRequest) -> User:
        email = data.email.lower()
        password_hash = await run_in_threadpool(_hash_password, data.password)
        try:
            async with self.session.begin():
                if await self.users.email_exists(email):
                    raise EmailAlreadyRegisteredError()
                role = await self.roles.get_by_name("user")
                if role is None:
                    raise RoleNotFoundError("user")
                return await self.users.add(
                    User(
                        **data.model_dump(exclude={"password", "email"}),
                        email=email, role_id=role.id, password_hash=password_hash,
                    )
                )
        except IntegrityError as exc:
            if getattr(exc.orig, "sqlstate", None) == "23505" and await self._email_exists(email):
                raise EmailAlreadyRegisteredError() from exc
            raise

    async def _email_exists(self, email: str) -> bool:
        async with self.session.begin():
            return await self.users.email_exists(email)

    async def login(self, email: str, password: str, previous_token: str | None = None) -> str:
        async with self.session.begin():
            user = await self.users.get_by_email(email.lower())
            verified = await run_in_threadpool(
                _verify_password, password, user.password_hash if user else None
            )
            if user is None or not user.is_active or not verified:
                raise InvalidCredentialsError()

            now = datetime.now(UTC)
            token = secrets.token_urlsafe(32)
            self.session.add(
                AuthSession(
                    token_hash=_token_hash(token), user_id=user.id,
                    expires_at=now + self.session_lifetime,
                )
            )
            user.last_login_at = now
            if previous_token:
                await self._revoke(previous_token, now)
        return token

    async def authenticate(self, token: str) -> AuthContext | None:
        async with self.session.begin():
            result = await self.session.execute(
                select(User.id, Role.name)
                .join(AuthSession, AuthSession.user_id == User.id)
                .join(Role, Role.id == User.role_id)
                .where(
                    AuthSession.token_hash == _token_hash(token),
                    AuthSession.revoked_at.is_(None),
                    AuthSession.expires_at > datetime.now(UTC),
                    User.is_active.is_(True),
                )
            )
            row = result.one_or_none()
            return AuthContext(*row) if row else None

    async def logout(self, token: str) -> None:
        async with self.session.begin():
            await self._revoke(token, datetime.now(UTC))

    async def _revoke(self, token: str, now: datetime) -> None:
        await self.session.execute(
            update(AuthSession)
            .where(AuthSession.token_hash == _token_hash(token), AuthSession.revoked_at.is_(None))
            .values(revoked_at=now)
        )
