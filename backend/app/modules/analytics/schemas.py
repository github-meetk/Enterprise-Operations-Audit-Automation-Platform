from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_audits: int
    open_audits: int
    high_risk_audits: int
    pending_workflow_tasks: int
    submitted_leave_requests: int
    submitted_expense_requests: int
    audit_statuses: dict[str, int]
