from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.errors import AppError
from app.modules.audit.models import Audit
from app.modules.audit.schemas import AuditCreate

TRANSITIONS = {
    "draft": {"planned", "cancelled"},
    "planned": {"in_progress", "cancelled"},
    "in_progress": {"under_review", "cancelled"},
    "under_review": {"approved", "in_progress", "cancelled"},
    "approved": {"closed"},
    "closed": set(),
    "cancelled": set(),
}


async def create_audit(db: AsyncSession, payload: AuditCreate) -> Audit:
    count = await db.scalar(select(func.count(Audit.id)))
    audit = Audit(
        **payload.model_dump(),
        reference=f"AUD-{datetime.now(UTC).year}-{(count or 0) + 1:06d}",
    )
    db.add(audit)
    await db.commit()
    await db.refresh(audit)
    return audit


async def transition_audit(db: AsyncSession, audit: Audit, target_status: str) -> Audit:
    if target_status not in TRANSITIONS[audit.status]:
        raise AppError(
            "AUDIT_INVALID_STATUS_TRANSITION",
            f"Audit cannot move from {audit.status} to {target_status}.",
            409,
        )
    audit.status = target_status
    audit.version += 1
    await db.commit()
    await db.refresh(audit)
    return audit
