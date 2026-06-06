from collections.abc import Callable

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.errors import AppError
from app.core.database import get_db_session
from app.core.security import decode_access_token, utc_now
from app.modules.identity.models import AuthSession, User
from app.modules.identity.service import list_permissions

bearer = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: AsyncSession = Depends(get_db_session),
) -> User:
    if not credentials:
        raise AppError("AUTH_REQUIRED", "Authentication is required.", 401)
    user_id, session_id = decode_access_token(credentials.credentials)
    session = await db.get(AuthSession, session_id)
    user = await db.get(User, user_id)
    if (
        not session
        or session.user_id != user_id
        or session.revoked_at
        or session.expires_at <= utc_now()
        or not user
        or not user.is_active
        or user.deleted_at
    ):
        raise AppError("AUTH_SESSION_EXPIRED", "Session is no longer active.", 401)
    return user


def require_permission(permission: str) -> Callable:
    async def dependency(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db_session),
    ) -> User:
        permissions = await list_permissions(db, user.id)
        if permission not in permissions:
            raise AppError("AUTH_FORBIDDEN", "You do not have permission for this action.", 403)
        return user

    return dependency
