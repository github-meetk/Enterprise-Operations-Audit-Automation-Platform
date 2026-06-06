from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Audit(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "audits"

    reference: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text, default="")
    audit_type: Mapped[str] = mapped_column(String(40), index=True)
    status: Mapped[str] = mapped_column(String(40), default="draft", index=True)
    risk_level: Mapped[str] = mapped_column(String(20), default="low", index=True)
    risk_score: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=0)
    department_id: Mapped[UUID] = mapped_column(ForeignKey("departments.id"), index=True)
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    lead_auditor_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    workflow_instance_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("workflow_instances.id"), nullable=True
    )
    planned_start_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    planned_end_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    version: Mapped[int] = mapped_column(Integer, default=1)


class AuditFinding(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "audit_findings"

    audit_id: Mapped[UUID] = mapped_column(ForeignKey("audits.id"), index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(String(20), index=True)
    status: Mapped[str] = mapped_column(String(40), default="open", index=True)
    remediation_owner_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
