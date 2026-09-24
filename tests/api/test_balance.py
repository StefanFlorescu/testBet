"""Tests for the balance endpoint."""

import pytest
from pytest_check import check


pytestmark = [pytest.mark.api, pytest.mark.balance]


def test_get_balance_endpoint_returns_success(get_balance) -> None:
    """Verify that an authenticated user can retrieve their balance."""
    check.equal(get_balance().status_code, 200, "Expected 200 OK response code")


def test_get_balance_returns_required_fields(get_balance) -> None:
    """Verify that the balance response contains its required fields."""
    response_body = get_balance().json()
    assert isinstance(response_body, dict), "Expected response body to be a dictionary"
    check.is_in("balance", response_body)
    check.is_in("currency", response_body)


def test_get_balance_returns_valid_balance_values(get_balance) -> None:
    """Verify that the balance is numeric and not negative."""
    response_body = get_balance().json()
    balance = response_body.get("balance")
    currency = response_body.get("currency")
    check.is_instance(balance, (int, float), f"Balance must be numeric: {balance}")
    check.greater_equal(balance, 0, f"Balance {balance} must not be negative")
    check.equal(currency, "EUR", f"Balance currency must be EUR: {currency}")
    
