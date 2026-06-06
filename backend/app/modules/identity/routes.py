from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.core.security import decode_access_token
from app.modules.identity.dependencies import bearer, get_current_user
from app.modules.identity.models import User
from app.modules.identity.schemas import (
    CurrentUserResponse,
    LoginRequest,
    RefreshRequest,
    TokenResponse,
)
from app.modules.identity.service import (
    authenticate,
    list_permissions,
    revoke_session,
    rotate_refresh_token,
)

router = APIRouter(prefix="/auth", tags=["identity"])


@router.post("/login", response_model=TokenResponse)
async def login(
    payload: LoginRequest, request: Request, db: AsyncSession = Depends(get_db_session)
):
    client_host = request.client.host if request.client else None
    access, refresh = await authenticate(
        db, payload.email, payload.password, request.headers.get("user-agent"), client_host
    )
    return TokenResponse(access_token=access, refresh_token=refresh)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(payload: RefreshRequest, db: AsyncSession = Depends(get_db_session)):
    access, replacement = await rotate_refresh_token(db, payload.refresh_token)
    return TokenResponse(access_token=access, refresh_token=replacement)


@router.post("/logout", status_code=204)
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    _: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> None:
    _, session_id = decode_access_token(credentials.credentials)
    await revoke_session(db, session_id)


@router.get("/me", response_model=CurrentUserResponse)
async def me(
    user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db_session)
):
    return CurrentUserResponse(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        employee_number=user.employee_number,
        job_title=user.job_title,
        permissions=await list_permissions(db, user.id),
    )
