from datetime import timedelta
from uuid import UUID, uuid4

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.errors import AppError
from app.core.config import get_settings
from app.core.security import (
    create_access_token,
    hash_refresh_token,
    new_refresh_token,
    utc_now,
    verify_password,
)
from app.modules.identity.models import AuthSession, RefreshToken, Role, User, UserRole

settings = get_settings()


async def authenticate(
    db: AsyncSession, email: str, password: str, user_agent: str | None, ip_address: str | None
) -> tuple[str, str]:
    user = await db.scalar(
        select(User).where(User.email == email.lower(), User.deleted_at.is_(None))
    )
    if not user or not user.is_active or not verify_password(password, user.password_hash):
        raise AppError("AUTH_INVALID_CREDENTIALS", "Email or password is incorrect.", 401)
    now = utc_now()
    session = AuthSession(
        user_id=user.id,
        user_agent=user_agent,
        ip_address=ip_address,
        last_activity_at=now,
        expires_at=now + timedelta(days=settings.refresh_token_ttl_days),
    )
    db.add(session)
    await db.flush()
    refresh = await _issue_refresh_token(db, session.id, uuid4())
    user.last_login_at = now
    await db.commit()
    return create_access_token(user.id, session.id), refresh


async def rotate_refresh_token(db: AsyncSession, raw_token: str) -> tuple[str, str]:
    now = utc_now()
    token = await db.scalar(
        select(RefreshToken)
        .where(RefreshToken.token_hash == hash_refresh_token(raw_token))
        .with_for_update()
    )
    if not token or token.revoked_at or token.expires_at <= now:
        raise AppError("AUTH_INVALID_REFRESH_TOKEN", "Refresh token is invalid or expired.", 401)
    session = await db.get(AuthSession, token.session_id)
    if not session or session.revoked_at or session.expires_at <= now:
        raise AppError("AUTH_SESSION_EXPIRED", "Session is no longer active.", 401)
    if token.consumed_at:
        await _revoke_family(db, token.token_family, now)
        session.revoked_at = now
        await db.commit()
        raise AppError("AUTH_REFRESH_REUSE_DETECTED", "Session was revoked for safety.", 401)
    token.consumed_at = now
    replacement_raw = await _issue_refresh_token(db, token.session_id, token.token_family)
    replacement = await db.scalar(
        select(RefreshToken).where(
            RefreshToken.token_hash == hash_refresh_token(replacement_raw)
        )
    )
    token.replaced_by_token_id = replacement.id if replacement else None
    session.last_activity_at = now
    await db.commit()
    return create_access_token(session.user_id, session.id), replacement_raw


async def revoke_session(db: AsyncSession, session_id: UUID) -> None:
    now = utc_now()
    session = await db.get(AuthSession, session_id)
    if session:
        session.revoked_at = now
        await db.execute(
            update(RefreshToken)
            .where(RefreshToken.session_id == session_id, RefreshToken.revoked_at.is_(None))
            .values(revoked_at=now)
        )
        await db.commit()


async def list_permissions(db: AsyncSession, user_id: UUID) -> list[str]:
    roles = (
        await db.scalars(
            select(UserRole)
            .where(UserRole.user_id == user_id, UserRole.deleted_at.is_(None))
            .options(selectinload(UserRole.role).selectinload(Role.permissions))
        )
    ).all()
    return sorted(
        {
            role_permission.permission.code
            for user_role in roles
            for role_permission in user_role.role.permissions
            if role_permission.deleted_at is None
        }
    )


async def _issue_refresh_token(db: AsyncSession, session_id: UUID, family: UUID) -> str:
    raw = new_refresh_token()
    db.add(
        RefreshToken(
            session_id=session_id,
            token_family=family,
            token_hash=hash_refresh_token(raw),
            expires_at=utc_now() + timedelta(days=settings.refresh_token_ttl_days),
        )
    )
    await db.flush()
    return raw


async def _revoke_family(db: AsyncSession, family: UUID, now) -> None:
    await db.execute(
        update(RefreshToken)
        .where(RefreshToken.token_family == family, RefreshToken.revoked_at.is_(None))
        .values(revoked_at=now)
    )
