from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AuditCreate(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    description: str = ""
    audit_type: str = Field(pattern="^(internal|external|regulatory|process)$")
    department_id: UUID
    owner_id: UUID
    lead_auditor_id: UUID | None = None
    planned_start_at: datetime | None = None
    planned_end_at: datetime | None = None


class AuditResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    reference: str
    title: str
    audit_type: str
    status: str
    risk_level: str
    risk_score: Decimal
    department_id: UUID
    lead_auditor_id: UUID | None
    planned_end_at: datetime | None


class AuditStatusUpdate(BaseModel):
    status: str = Field(pattern="^(planned|in_progress|under_review|approved|closed|cancelled)$")
