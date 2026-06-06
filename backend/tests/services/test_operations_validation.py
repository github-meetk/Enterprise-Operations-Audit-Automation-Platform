from datetime import date

import pytest
from pydantic import ValidationError

from app.modules.operations.schemas import LeaveRequestCreate


def test_leave_request_rejects_inverted_dates() -> None:
    with pytest.raises(ValidationError):
        LeaveRequestCreate(
            department_id="00000000-0000-0000-0000-000000000001",
            leave_type="annual",
            start_date=date(2026, 6, 10),
            end_date=date(2026, 6, 9),
        )
