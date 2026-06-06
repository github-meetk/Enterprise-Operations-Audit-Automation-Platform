from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.modules.analytics.schemas import DashboardSummary
from app.modules.audit.models import Audit
from app.modules.identity.dependencies import get_current_user
from app.modules.identity.models import User
from app.modules.operations.models import ExpenseRequest, LeaveRequest
from app.modules.workflow.models import WorkflowTask

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/dashboard", response_model=DashboardSummary)
async def dashboard(
    _: User = Depends(get_current_user), db: AsyncSession = Depends(get_db_session)
) -> DashboardSummary:
    status_counts = select(Audit.status, func.count(Audit.id)).group_by(Audit.status)
    rows = (await db.execute(status_counts)).all()
    audit_statuses = {status: count for status, count in rows}
    return DashboardSummary(
        total_audits=sum(audit_statuses.values()),
        open_audits=sum(v for k, v in audit_statuses.items() if k not in {"closed", "cancelled"}),
        high_risk_audits=await db.scalar(
            select(func.count(Audit.id)).where(Audit.risk_level.in_(["high", "critical"]))
        )
        or 0,
        pending_workflow_tasks=await db.scalar(
            select(func.count(WorkflowTask.id)).where(WorkflowTask.status == "pending")
        )
        or 0,
        submitted_leave_requests=await db.scalar(
            select(func.count(LeaveRequest.id)).where(LeaveRequest.status == "submitted")
        )
        or 0,
        submitted_expense_requests=await db.scalar(
            select(func.count(ExpenseRequest.id)).where(ExpenseRequest.status == "submitted")
        )
        or 0,
        audit_statuses=audit_statuses,
    )
