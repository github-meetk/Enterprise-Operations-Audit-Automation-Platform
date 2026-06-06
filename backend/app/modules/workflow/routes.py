from datetime import UTC, datetime
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.errors import AppError
from app.core.database import get_db_session
from app.modules.identity.dependencies import get_current_user
from app.modules.identity.models import User
from app.modules.workflow.models import WorkflowTask, WorkflowTaskAction
from app.modules.workflow.schemas import WorkflowTaskActionRequest, WorkflowTaskResponse

router = APIRouter(prefix="/workflow-tasks", tags=["workflow"])


@router.get("/mine", response_model=list[WorkflowTaskResponse])
async def my_tasks(
    user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db_session)
):
    return (
        await db.scalars(
            select(WorkflowTask)
            .where(WorkflowTask.assignee_id == user.id, WorkflowTask.deleted_at.is_(None))
            .order_by(WorkflowTask.due_at.asc().nullslast())
        )
    ).all()


@router.post("/{task_id}/actions", response_model=WorkflowTaskResponse)
async def act_on_task(
    task_id: UUID,
    payload: WorkflowTaskActionRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    task = await db.scalar(select(WorkflowTask).where(WorkflowTask.id == task_id).with_for_update())
    if not task or task.assignee_id != user.id:
        raise AppError("WORKFLOW_TASK_NOT_FOUND", "Workflow task was not found.", 404)
    if task.status != "pending":
        raise AppError("WORKFLOW_TASK_ALREADY_COMPLETED", "Task has already been actioned.", 409)
    task.status = "approved" if payload.action == "approve" else "rejected"
    task.completed_at = datetime.now(UTC)
    db.add(
        WorkflowTaskAction(
            task_id=task.id,
            actor_id=user.id,
            action=payload.action,
            comment=payload.comment,
            created_at=datetime.now(UTC),
        )
    )
    await db.commit()
    await db.refresh(task)
    return task
