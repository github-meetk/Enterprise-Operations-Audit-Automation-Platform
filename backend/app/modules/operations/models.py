from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, TimestampMixin, UUIDPrimaryKeyMixin


class LeaveRequest(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "leave_requests"

    requester_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    department_id: Mapped[UUID] = mapped_column(ForeignKey("departments.id"), index=True)
    leave_type: Mapped[str] = mapped_column(String(40))
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    reason: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(30), default="submitted", index=True)
    workflow_instance_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("workflow_instances.id"), nullable=True
    )


class ExpenseRequest(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "expense_requests"

    requester_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    department_id: Mapped[UUID] = mapped_column(ForeignKey("departments.id"), index=True)
    purpose: Mapped[str] = mapped_column(String(255))
    total_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    currency_code: Mapped[str] = mapped_column(String(3))
    expense_date: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(30), default="submitted", index=True)
    workflow_instance_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("workflow_instances.id"), nullable=True
    )


class TravelRequest(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "travel_requests"

    requester_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    department_id: Mapped[UUID] = mapped_column(ForeignKey("departments.id"), index=True)
    origin: Mapped[str] = mapped_column(String(150))
    destination: Mapped[str] = mapped_column(String(150))
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    estimated_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    currency_code: Mapped[str] = mapped_column(String(3))
    status: Mapped[str] = mapped_column(String(30), default="submitted", index=True)
    workflow_instance_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("workflow_instances.id"), nullable=True
    )


class EmployeeTask(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "employee_tasks"

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text, default="")
    assigner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    assignee_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    department_id: Mapped[UUID] = mapped_column(ForeignKey("departments.id"), index=True)
    priority: Mapped[str] = mapped_column(String(20), default="medium")
    status: Mapped[str] = mapped_column(String(30), default="open", index=True)
    due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
