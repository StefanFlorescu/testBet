"""Tests for the matches endpoint."""

from datetime import date, datetime, UTC
import pytest
from pytest_check import check
pytestmark = [pytest.mark.matches, pytest.mark.api]

odds_keys = ("home", "draw", "away")


def test_get_matches_returns_success(get_matches) -> None:
    """Verify that an authenticated user can retrieve upcoming matches."""
    response = get_matches()
    check.equal(response.status_code, 200, "Expected 200 OK response code")
    check.is_instance(response.json(), list, "Expected response body to be a list of matches")


def test_get_matches_returns_required_match_fields(get_matches) -> None:
    """Verify that every returned match contains the documented fields."""

    matches = get_matches().json()

    check.is_true(matches, "Expected at least one upcoming match")
    for match in matches:
        check.is_instance(match, dict)
        check.is_true(match.get("id"), "Match ID must be present and non-empty")
        check.is_true(match.get("competition"), "Competition must be present")
        check.is_true(match.get("homeTeam"), "Home team must be present")
        check.is_true(match.get("awayTeam"), "Away team must be present")
        check.is_instance(match.get("kickoffDate"), str)
        check.is_instance(match.get("odds"), dict, "Odds must be present and of dictionary type")

# TODO - report on the critical bug - the kickoffDate is not in the future
def test_get_matches_returns_valid_kickoff_dates(
    get_matches,
) -> None:
    """Verify that kickoff dates use the documented YYYY-MM-DD format and is in the future."""

    matches = get_matches().json()

    for match in matches:
        kickoff_date = match.get("kickoffDate", None)
        assert kickoff_date is not None, "kickoffDate must be present"
        try:
            parsed_date = date.fromisoformat(kickoff_date)
            check.greater(
                parsed_date,
                datetime.now(tz=UTC).date(),
                f"kickoffDate must be in the future: {kickoff_date}",
            )
        except ValueError:
            check.fail(f"Invalid kickoffDate format: {kickoff_date}")


def test_get_matches_returns_valid_odds(
    get_matches,
) -> None:
    """Verify that each match exposes HOME, DRAW, and AWAY in match odds."""

    matches = get_matches().json()

    for match in matches:
        odds = match.get("odds")
        check.is_instance(odds, dict)
        if isinstance(odds, dict):
            for outcome in odds_keys:
                check.is_in(outcome, odds)
                value = odds.get(outcome)
                assert isinstance(value, (int, float)), f'Expected {outcome} value to be a float'
                check.greater_equal(value, 1.0)
                check.less_equal(value, 100.0)
