"""Positive tests for the reset-balance endpoint."""

import pytest
from pytest_check import check


pytestmark = [pytest.mark.api, pytest.mark.balance]

expected_response_keys = ("message", "balance", "currency")


def test_reset_balance_returns_success(reset_balance) -> None:
    """Verify that the endpoint returns a successful response and correct body."""
    response = reset_balance()
    check.equal(response.status_code, 200)
    response_body = response.json()
    assert isinstance(response_body, dict), "Expected response body to be a dictionary"
    for key in expected_response_keys:
        check.is_in(key, response_body, f"Expected '{key}' in response body")


def test_reset_balance_returns_valid_balance(reset_balance) -> None:
    """Verify that the reset balance is numeric and non-negative."""
    response_body = reset_balance().json()
    balance = response_body.get("balance")
    currency = response_body.get("currency")
    message = response_body.get("message")
    check.is_instance(balance, (int, float), f"Balance must be numeric: {balance}")
    check.greater_equal(balance, 0)
    check.equal(currency, "EUR", f"Balance currency must be EUR: {currency}")
    check.equal(message, "Balance reset successfully", f"Unexpected message: {message}")
