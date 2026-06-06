"""Registers SQLAlchemy mappings for migrations and startup tooling."""

from app.modules.audit.models import Audit, AuditFinding
from app.modules.identity.models import (
    AuthSession,
    Permission,
    RefreshToken,
    Role,
    RolePermission,
    User,
    UserRole,
)
from app.modules.notification.models import Notification
from app.modules.operations.models import EmployeeTask, ExpenseRequest, LeaveRequest, TravelRequest
from app.modules.organization.models import Department, DepartmentMembership
from app.modules.workflow.models import (
    WorkflowDefinition,
    WorkflowDefinitionVersion,
    WorkflowInstance,
    WorkflowStep,
    WorkflowTask,
    WorkflowTaskAction,
)
from app.platform.models import ActivityLog, OutboxEvent

__all__ = [
    "ActivityLog",
    "Audit",
    "AuditFinding",
    "AuthSession",
    "Department",
    "DepartmentMembership",
    "EmployeeTask",
    "ExpenseRequest",
    "LeaveRequest",
    "Notification",
    "OutboxEvent",
    "Permission",
    "RefreshToken",
    "Role",
    "RolePermission",
    "TravelRequest",
    "User",
    "UserRole",
    "WorkflowDefinition",
    "WorkflowDefinitionVersion",
    "WorkflowInstance",
    "WorkflowStep",
    "WorkflowTask",
    "WorkflowTaskAction",
]
