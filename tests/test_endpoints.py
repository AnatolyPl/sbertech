import json

from fastapi.testclient import TestClient
import parametrize_from_file

from backend.app import app

client = TestClient(app)


@parametrize_from_file
def test_monthly_deposit_periods_amount_v1_validation_error(request_body, expected_response):

    response = client.post("/v1/deposits/monthly", content=json.dumps(request_body))
    assert response.status_code == 400
    assert response.json() == expected_response


@parametrize_from_file
def test_monthly_deposit_periods_amount_v1_correct(request_body, expected_response):

    response = client.post("/v1/deposits/monthly", content=json.dumps(request_body))
    assert response.status_code == 200
    assert response.json() == expected_response


@parametrize_from_file
def test_monthly_deposit_periods_amount_v2_validation_error(query_params, expected_response):

    response = client.get("/v2/deposits/monthly", params=query_params)
    assert response.status_code == 400
    assert response.json() == expected_response


@parametrize_from_file
def test_monthly_deposit_periods_amount_v2_correct(query_params, expected_response):

    response = client.get("/v2/deposits/monthly", params=query_params)
    assert response.status_code == 200
    assert response.json() == expected_response
