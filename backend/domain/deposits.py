from abc import ABC, abstractmethod

from datetime import date
from dateutil import relativedelta
from dataclasses import dataclass, asdict
from typing import List

from backend import get_logger


logger = get_logger(__name__)


@dataclass
class DepositPeriodAmount:
    date: date
    amount: float

    def dict(self):
        return asdict(self)


class MonthlyDeposit:
    MAX_PERIODS = 60
    MIN_PERIODS = 1

    MAX_AMOUNT = 3000000
    MIN_AMOUNT = 10000

    MAX_ANNUAL_RATE = 8
    MIN_ANNUAL_RATE = 1

    def __init__(
        self, start_date: date, periods: int, amount: int, monthly_rate: float
    ):
        self.start_date = start_date
        self.periods = periods
        self.start_amount = amount
        self.monthly_rate = monthly_rate
        self.deposit_periods_amount = self._calculate_deposit_periods_amount()
        logger.info("Monthly deposit object created successfully")

    @classmethod
    def from_annual_rate(
        cls, start_date: date, periods: int, amount: int, annual_rate: float
    ):
        logger.info("Creating monthly deposit suing annual rate")
        if annual_rate < cls.MIN_ANNUAL_RATE or annual_rate > cls.MAX_ANNUAL_RATE:
            raise ValueError(
                f"Annual rate should be between [{cls.MIN_ANNUAL_RATE}, {cls.MAX_ANNUAL_RATE}]"
            )

        monthly_rate = annual_rate / 12 / 100

        return cls(
            start_date=start_date,
            periods=periods,
            amount=amount,
            monthly_rate=monthly_rate,
        )

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        if not isinstance(start_date, date):
            raise ValueError(
                f"Start_date should be 'date' type. {type(start_date)} type given"
            )
        self._start_date = start_date

    @property
    def periods(self):
        return self._periods

    @periods.setter
    def periods(self, periods):
        if periods < self.MIN_PERIODS or periods > self.MAX_PERIODS:
            raise ValueError(
                f"Number of periods should be between [{self.MIN_PERIODS}, {self.MAX_PERIODS}]"
            )
        self._periods = periods

    @property
    def start_amount(self):
        return self._start_amount

    @start_amount.setter
    def start_amount(self, start_amount):
        if start_amount < self.MIN_AMOUNT or start_amount > self.MAX_AMOUNT:
            raise ValueError(
                f"Start amount should be between [{self.MIN_AMOUNT}, {self.MAX_AMOUNT}]"
            )
        self._start_amount = start_amount

    @property
    def monthly_rate(self):
        return self._monthly_rate

    @monthly_rate.setter
    def monthly_rate(self, monthly_rate):
        if (
            monthly_rate < self.MIN_ANNUAL_RATE / 12 / 100
            or monthly_rate > self.MAX_ANNUAL_RATE / 12 / 100
        ):
            raise ValueError(
                f"Annual rate should be between [{self.MIN_ANNUAL_RATE}, "
                f"{self.MAX_ANNUAL_RATE}]. {monthly_rate * 12 * 100} given "
            )
        self._monthly_rate = monthly_rate

    def _calculate_deposit_periods_amount(self) -> List[DepositPeriodAmount]:
        periods_amount = []

        for i in range(1, self.periods + 1):
            next_date = self.start_date + relativedelta.relativedelta(months=i)
            next_amount = self.start_amount * (1 + self.monthly_rate) ** i
            periods_amount.append(
                DepositPeriodAmount(date=next_date, amount=round(next_amount, 2))
            )

        return periods_amount
