import hashlib
import secrets
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from jose import JWTError, jwt
from pwdlib import PasswordHash

from app.api.errors import AppError
from app.core.config import get_settings

settings = get_settings()
password_hash = PasswordHash.recommended()
ALGORITHM = "HS256"


def utc_now() -> datetime:
    return datetime.now(UTC)


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, encoded_hash: str) -> bool:
    return password_hash.verify(password, encoded_hash)


def create_access_token(user_id: UUID, session_id: UUID) -> str:
    issued_at = utc_now()
    return jwt.encode(
        {
            "sub": str(user_id),
            "sid": str(session_id),
            "type": "access",
            "iat": issued_at,
            "exp": issued_at + timedelta(minutes=settings.access_token_ttl_minutes),
            "jti": str(uuid4()),
        },
        settings.secret_key,
        algorithm=ALGORITHM,
    )


def decode_access_token(token: str) -> tuple[UUID, UUID]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            raise ValueError("Invalid token type")
        return UUID(payload["sub"]), UUID(payload["sid"])
    except (JWTError, KeyError, TypeError, ValueError) as exc:
        raise AppError("AUTH_INVALID_TOKEN", "Access token is invalid or expired.", 401) from exc


def new_refresh_token() -> str:
    return secrets.token_urlsafe(48)


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()
