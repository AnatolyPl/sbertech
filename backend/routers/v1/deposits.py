from __future__ import annotations

from logging import getLogger
from fastapi import APIRouter

from backend.pydantic_models.v1.deposits import (
    MonthlyDepositBodyParams,
    MonthlyDepositPostResponse
)

from backend.domain.deposits import MonthlyDeposit

logger = getLogger(__name__)
router = APIRouter(prefix='/deposits', tags=['Deposits'])


@router.post(
    '/monthly',
    response_model=MonthlyDepositPostResponse,
)
def get_monthly_deposit_periods_amount(
    body_params: MonthlyDepositBodyParams
) -> MonthlyDepositPostResponse:

    monthly_deposit = MonthlyDeposit.from_annual_rate(
        amount=body_params.amount,
        start_date=body_params.start_date,
        periods=body_params.periods,
        annual_rate=body_params.rate
    )

    return MonthlyDepositPostResponse.from_domain_entity(monthly_deposit.deposit_periods_amount)
