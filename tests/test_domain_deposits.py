from datetime import datetime
import parametrize_from_file
import pytest

from backend.domain.deposits import MonthlyDeposit


@parametrize_from_file
def test_monthly_deposit_validation_error(init_params):
    with pytest.raises(ValueError):
        init_params["start_date"] = datetime.strptime(init_params["start_date"], "%Y-%m-%d").date()
        MonthlyDeposit.from_annual_rate(**init_params)


@parametrize_from_file
def test_monthly_deposit_success_initialization(init_params, expected_deposit_periods_amount):
    init_params["start_date"] = datetime.strptime(init_params["start_date"], "%Y-%m-%d").date()
    monthly_deposit = MonthlyDeposit.from_annual_rate(**init_params)

    assert len(monthly_deposit.deposit_periods_amount) == len(expected_deposit_periods_amount)

    for deposit_period_amount, expected_deposit_period_amount in zip(
        monthly_deposit.deposit_periods_amount,
        expected_deposit_periods_amount
    ):
        expected_deposit_period_amount["date"] = datetime.strptime(expected_deposit_period_amount["date"],
                                                                   "%Y-%m-%d").date()
        assert deposit_period_amount.dict() == expected_deposit_period_amount
