from __future__ import annotations

from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Department(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "departments"

    code: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(150))
    parent_id: Mapped[UUID | None] = mapped_column(ForeignKey("departments.id"), nullable=True)
    manager_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)


class DepartmentMembership(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "department_memberships"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    department_id: Mapped[UUID] = mapped_column(ForeignKey("departments.id"), index=True)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)

    department: Mapped[Department] = relationship(lazy="joined")
