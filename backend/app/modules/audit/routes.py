from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.errors import AppError
from app.core.database import get_db_session
from app.modules.audit.models import Audit
from app.modules.audit.schemas import AuditCreate, AuditResponse, AuditStatusUpdate
from app.modules.audit.service import create_audit, transition_audit
from app.modules.identity.dependencies import get_current_user, require_permission
from app.modules.identity.models import User

router = APIRouter(prefix="/audits", tags=["audits"])


@router.get("", response_model=list[AuditResponse])
async def list_audits(
    status: str | None = None,
    department_id: UUID | None = None,
    limit: int = Query(default=50, ge=1, le=100),
    _: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    query = select(Audit).where(Audit.deleted_at.is_(None)).limit(limit)
    if status:
        query = query.where(Audit.status == status)
    if department_id:
        query = query.where(Audit.department_id == department_id)
    return (await db.scalars(query.order_by(Audit.created_at.desc()))).all()


@router.post("", response_model=AuditResponse, status_code=201)
async def create(
    payload: AuditCreate,
    _: User = Depends(require_permission("audit:audit:create")),
    db: AsyncSession = Depends(get_db_session),
):
    return await create_audit(db, payload)


@router.patch("/{audit_id}/status", response_model=AuditResponse)
async def update_status(
    audit_id: UUID,
    payload: AuditStatusUpdate,
    _: User = Depends(require_permission("audit:audit:update")),
    db: AsyncSession = Depends(get_db_session),
):
    audit = await db.get(Audit, audit_id)
    if not audit or audit.deleted_at:
        raise AppError("AUDIT_NOT_FOUND", "Audit was not found.", 404)
    return await transition_audit(db, audit, payload.status)
