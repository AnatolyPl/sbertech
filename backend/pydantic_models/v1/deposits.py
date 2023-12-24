from __future__ import annotations

from datetime import date, datetime
from typing import List, Dict
from pydantic import BaseModel, Field, RootModel, field_validator, field_serializer

from backend.domain.deposits import DepositPeriodAmount


class MonthlyDepositBodyParams(BaseModel):
    start_date: date = Field(
        description="dd.mm.YYYY format supported only", alias="date"
    )
    periods: int = Field(ge=1, le=60)
    amount: int = Field(ge=10000, le=3000000)
    rate: float = Field(ge=1, le=8)

    @field_validator("start_date", mode="before")
    def parse_start_date(cls, value):
        return datetime.strptime(value, "%d.%m.%Y").date()


class MonthlyDepositPostResponse(RootModel):
    root: Dict[date, float]

    @classmethod
    def from_domain_entity(cls, monthly_periods_amount: List[DepositPeriodAmount]):
        return cls.model_validate(
            {
                month_period_amount.date: month_period_amount.amount
                for month_period_amount in monthly_periods_amount
            }
        )

    @field_serializer("root")
    def serialize_root(self, root: Dict[date, float], _info):
        return {k.strftime("%d.%m.%Y"): v for k, v in root.items()}
