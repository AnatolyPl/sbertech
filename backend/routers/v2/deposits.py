from __future__ import annotations

from logging import getLogger
from fastapi import APIRouter, Depends

from backend.pydantic_models.v2.deposits import (
    MonthlyDepositQueryParams,
    MonthlyDepositGetResponse,
)
from backend.domain.deposits import MonthlyDeposit

logger = getLogger(__name__)
router = APIRouter(prefix="/deposits", tags=["Deposits"])


@router.get(
    "/monthly",
    response_model=MonthlyDepositGetResponse,
)
def get_monthly_deposit_periods_amount(
    query_params: MonthlyDepositQueryParams = Depends(),
) -> MonthlyDepositGetResponse:
    monthly_deposit = MonthlyDeposit.from_annual_rate(
        amount=query_params.amount,
        start_date=query_params.start_date,
        periods=query_params.periods,
        annual_rate=query_params.rate,
    )

    return MonthlyDepositGetResponse.from_domain_entity(
        monthly_deposit.deposit_periods_amount
    )
