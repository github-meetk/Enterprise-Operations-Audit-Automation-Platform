from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.modules.identity.dependencies import get_current_user
from app.modules.identity.models import User
from app.modules.operations.models import ExpenseRequest, LeaveRequest
from app.modules.operations.schemas import (
    ExpenseRequestCreate,
    ExpenseRequestResponse,
    LeaveRequestCreate,
    LeaveRequestResponse,
)

router = APIRouter(prefix="/operations", tags=["operations"])


@router.get("/leave-requests/mine", response_model=list[LeaveRequestResponse])
async def my_leave_requests(
    user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db_session)
):
    return (
        await db.scalars(
            select(LeaveRequest)
            .where(LeaveRequest.requester_id == user.id, LeaveRequest.deleted_at.is_(None))
            .order_by(LeaveRequest.created_at.desc())
        )
    ).all()


@router.post("/leave-requests", response_model=LeaveRequestResponse, status_code=201)
async def create_leave_request(
    payload: LeaveRequestCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    request = LeaveRequest(requester_id=user.id, **payload.model_dump())
    db.add(request)
    await db.commit()
    await db.refresh(request)
    return request


@router.get("/expense-requests/mine", response_model=list[ExpenseRequestResponse])
async def my_expense_requests(
    user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db_session)
):
    return (
        await db.scalars(
            select(ExpenseRequest)
            .where(ExpenseRequest.requester_id == user.id, ExpenseRequest.deleted_at.is_(None))
            .order_by(ExpenseRequest.created_at.desc())
        )
    ).all()


@router.post("/expense-requests", response_model=ExpenseRequestResponse, status_code=201)
async def create_expense_request(
    payload: ExpenseRequestCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    request = ExpenseRequest(
        requester_id=user.id,
        currency_code=payload.currency_code.upper(),
        **payload.model_dump(exclude={"currency_code"}),
    )
    db.add(request)
    await db.commit()
    await db.refresh(request)
    return request
