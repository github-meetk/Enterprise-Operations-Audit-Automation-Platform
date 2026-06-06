import asyncio

from sqlalchemy import select

from app.core.database import async_session_factory
from app.core.security import hash_password
from app.modules.identity.models import Permission, Role, RolePermission, User, UserRole
from app.modules.organization.models import Department, DepartmentMembership
from app.modules.workflow.models import WorkflowDefinition, WorkflowDefinitionVersion

PERMISSIONS = [
    "audit:audit:create",
    "audit:audit:update",
    "audit:audit:view",
    "workflow:task:approve",
    "operations:request:create",
    "analytics:kpi:view",
]

ROLE_PERMISSIONS = {
    "admin": PERMISSIONS,
    "auditor": ["audit:audit:view", "audit:audit:update", "analytics:kpi:view"],
    "manager": ["workflow:task:approve", "operations:request:create", "analytics:kpi:view"],
    "employee": ["operations:request:create"],
    "compliance_officer": [
        "audit:audit:create",
        "audit:audit:update",
        "audit:audit:view",
        "analytics:kpi:view",
    ],
}


async def seed() -> None:
    async with async_session_factory() as db:
        permissions = {}
        for code in PERMISSIONS:
            item = await db.scalar(select(Permission).where(Permission.code == code))
            if not item:
                item = Permission(code=code, description=code.replace(":", " ").title())
                db.add(item)
                await db.flush()
            permissions[code] = item

        roles = {}
        for code, granted in ROLE_PERMISSIONS.items():
            role = await db.scalar(select(Role).where(Role.code == code))
            if not role:
                role = Role(code=code, name=code.replace("_", " ").title())
                db.add(role)
                await db.flush()
            roles[code] = role
            for permission_code in granted:
                existing = await db.scalar(
                    select(RolePermission).where(
                        RolePermission.role_id == role.id,
                        RolePermission.permission_id == permissions[permission_code].id,
                    )
                )
                if not existing:
                    db.add(
                        RolePermission(
                            role_id=role.id, permission_id=permissions[permission_code].id
                        )
                    )

        department = await db.scalar(select(Department).where(Department.code == "COMPLIANCE"))
        if not department:
            department = Department(code="COMPLIANCE", name="Compliance")
            db.add(department)
            await db.flush()

        user = await db.scalar(select(User).where(User.email == "admin@example.com"))
        if not user:
            user = User(
                email="admin@example.com",
                password_hash=hash_password("ChangeMe123!"),
                first_name="Platform",
                last_name="Admin",
                employee_number="EMP-0001",
                job_title="Platform Administrator",
            )
            db.add(user)
            await db.flush()
            db.add(
                DepartmentMembership(
                    user_id=user.id, department_id=department.id, is_primary=True
                )
            )
            db.add(
                UserRole(user_id=user.id, role_id=roles["admin"].id, department_id=department.id)
            )

        workflow = await db.scalar(
            select(WorkflowDefinition).where(WorkflowDefinition.key == "audit-approval")
        )
        if not workflow:
            workflow = WorkflowDefinition(
                key="audit-approval", name="Audit Approval", target_type="audit"
            )
            db.add(workflow)
            await db.flush()
            db.add(
                WorkflowDefinitionVersion(
                    definition_id=workflow.id,
                    version=1,
                    status="published",
                    config={"strategy": "compliance-officer-approval"},
                )
            )
        await db.commit()


if __name__ == "__main__":
    asyncio.run(seed())
