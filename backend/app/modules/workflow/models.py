from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, TimestampMixin, UUIDPrimaryKeyMixin


class WorkflowDefinition(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "workflow_definitions"

    key: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(180))
    target_type: Mapped[str] = mapped_column(String(80), index=True)
    description: Mapped[str] = mapped_column(Text, default="")


class WorkflowDefinitionVersion(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "workflow_definition_versions"
    __table_args__ = (UniqueConstraint("definition_id", "version"),)

    definition_id: Mapped[UUID] = mapped_column(ForeignKey("workflow_definitions.id"), index=True)
    version: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(30), default="draft", index=True)
    config: Mapped[dict] = mapped_column(JSONB, default=dict)


class WorkflowStep(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "workflow_steps"

    definition_version_id: Mapped[UUID] = mapped_column(
        ForeignKey("workflow_definition_versions.id"), index=True
    )
    key: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(180))
    step_type: Mapped[str] = mapped_column(String(40), default="approval")
    position: Mapped[int] = mapped_column(Integer)
    config: Mapped[dict] = mapped_column(JSONB, default=dict)


class WorkflowInstance(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "workflow_instances"

    definition_version_id: Mapped[UUID] = mapped_column(
        ForeignKey("workflow_definition_versions.id"), index=True
    )
    target_type: Mapped[str] = mapped_column(String(80), index=True)
    target_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), index=True)
    initiated_by_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String(30), default="running", index=True)
    current_step_key: Mapped[str | None] = mapped_column(String(100), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class WorkflowTask(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "workflow_tasks"

    instance_id: Mapped[UUID] = mapped_column(ForeignKey("workflow_instances.id"), index=True)
    step_id: Mapped[UUID | None] = mapped_column(ForeignKey("workflow_steps.id"), nullable=True)
    assignee_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    title: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(30), default="pending", index=True)
    due_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class WorkflowTaskAction(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "workflow_task_actions"

    task_id: Mapped[UUID] = mapped_column(ForeignKey("workflow_tasks.id"), index=True)
    actor_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    action: Mapped[str] = mapped_column(String(30))
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
