from __future__ import annotations

from datetime import date
from typing import List

from pydantic import BaseModel, Field

from backend.domain.deposits import DepositPeriodAmount


class MonthlyDepositQueryParams(BaseModel):
    start_date: date = Field(alias="date")
    periods: int = Field(ge=1, le=60)
    amount: int = Field(ge=10000, le=3000000)
    rate: float = Field(ge=1, le=8)


class MonthlyDeposit(BaseModel):
    date: date
    amount: float


class MonthlyDepositGetResponse(BaseModel):
    depositAmountMonthly: List[MonthlyDeposit]

    @classmethod
    def from_domain_entity(cls, monthly_periods_amount: List[DepositPeriodAmount]):
        return cls.model_validate(
            {
                "depositAmountMonthly": [
                    month_period_amount.dict()
                    for month_period_amount in monthly_periods_amount
                ]
            }
        )
