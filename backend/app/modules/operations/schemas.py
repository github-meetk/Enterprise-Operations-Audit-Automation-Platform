from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class LeaveRequestCreate(BaseModel):
    department_id: UUID
    leave_type: str = Field(pattern="^(annual|sick|personal|unpaid)$")
    start_date: date
    end_date: date
    reason: str = Field(default="", max_length=2000)

    @model_validator(mode="after")
    def valid_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("end_date must not precede start_date")
        return self


class LeaveRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    requester_id: UUID
    department_id: UUID
    leave_type: str
    start_date: date
    end_date: date
    status: str


class ExpenseRequestCreate(BaseModel):
    department_id: UUID
    purpose: str = Field(min_length=3, max_length=255)
    total_amount: Decimal = Field(gt=0)
    currency_code: str = Field(min_length=3, max_length=3)
    expense_date: date


class ExpenseRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    requester_id: UUID
    purpose: str
    total_amount: Decimal
    currency_code: str
    expense_date: date
    status: str
