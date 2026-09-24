"""Negative tests for the place-bet endpoint."""

import pytest
from pytest_check import check
import random
from src.logger import get_logger


logger = get_logger('test_place_bet')

MAX_STAKE = 100
MIN_STAKE = 1

def choose_stake(balance: float): 
    if balance >=MAX_STAKE:
        return MAX_STAKE
    return balance - 1

valid_selections = lambda: random.choice(("HOME", "DRAW", "AWAY"))

expected_success_fields = (
            "message",
            "matchId",
            "selection",
            "stake",
            "odds",
            "payout",
            "balance",
            "currency",
        )

invalid_stake_scenarios = [(None, "Stake must be a valid number."),
                           ('', "Stake must be a valid number."),
                           ("abc", "Stake must be a valid number."),
                           ("ten", "Stake must be a valid number."),
                           (-10, "Stake must be a positive number."),
                           (0, "Stake must be at least 1.00."),
                           (0.99, "Stake must be at least 1.00."),
                           (MAX_STAKE + 0.01, "Stake must be at most 100.00."),
                           (MAX_STAKE + 1.00, "Stake must be at most 100.00.")
                           ]

pytestmark = [pytest.mark.api, pytest.mark.bets]

def test_place_empty_payload_rejected(place_bet) -> None:
    """Verify that an empty payload is rejected."""

    response = place_bet()
    _response_body = response.json()
    error_type = _response_body.get("error")
    error_message = _response_body.get("message")
    check.equal(response.status_code, 422)
    check.equal(error_type, "invalid_match_id")
    check.equal(error_message, "Match id is invalid.")

# TODO -> defect match_id is not validated correctly, can use non-existent match_id and the validation error does not flag this
@pytest.mark.parametrize("match_id", ["", "unknown-match-id"])
def test_place_bet_rejects_invalid_match_id(place_bet, match_id: str) -> None:
    """Verify that blank and unknown match IDs are rejected."""
    response = place_bet(matchId=match_id)
    _response_body = response.json()
    error_type = _response_body.get("error")
    error_message = _response_body.get("message")
    check.equal(response.status_code, 422)
    check.equal(error_type, "invalid_match_id", f"Unexpected error type for match_id={match_id}: {error_type}")
    check.equal(error_message, "Match id is invalid.", f"Unexpected error message for match_id={match_id}: {error_message}")


def test_place_bet_rejects_missing_or_invalid_selection(place_bet) -> None:
    """Verify that a missing match ID is rejected."""
    response = place_bet(matchId="unknown-match-id")
    check.equal(response.status_code, 422)
    check.equal(response.json(), {"error":"invalid_selection","message":"Selection must be one of: HOME, DRAW, AWAY."})
    response = place_bet(selection="NOT", matchId="unknown-match-id")
    check.equal(response.status_code, 422)
    check.equal(response.json(), {"error":"invalid_selection","message":"Selection must be one of: HOME, DRAW, AWAY."})

def test_place_bet_rejects_missing_stake(place_bet) -> None:
    """Verify that a missing stake is rejected."""
    response = place_bet(matchId='unknown-match-id', selection=valid_selections())
    check.equal(response.status_code, 422)
    check.is_in("Stake must be a valid number.", response.text, f"Expected 'error' in response body for missing stake: {response.text}")

# TODO -> negative values for stake are not validated correctly, the validation error does not flag this
@pytest.mark.parametrize("stake, expected_message", invalid_stake_scenarios, ids=[f"stake={s[0]}" for s in invalid_stake_scenarios])
def test_place_bet_rejects_invalid_stake(place_bet, stake, expected_message: str) -> None:
    """Verify that invalid stake values are rejected."""
    response = place_bet( matchId='unknown-match-id', selection=valid_selections(), stake=stake)
    check.equal(response.status_code, 422)
    check.is_in(expected_message, response.text, f"Expected 'error' in response body for stake={stake}: {response.text}")

def test_place_bet_with_invalid_match_id(place_bet, valid_random_stakes) -> None:
    """Verify that only required fields are needed to place a bet."""
    response = place_bet(matchId='unknown-match-id', selection=valid_selections(), stake=valid_random_stakes())
    check.equal(response.status_code, 422)
    check.is_in("Match not found.", response.text, f"Expected 'error' in response body for missing stake: {response.text}")

# TODO -> defect (critical) the stake validation is not working correctly, can place a bet with a stake greater than the available balance
def test_place_bet_with_exceeding_stake(place_bet, get_balance, get_matches) -> None:
    matches = get_matches().json()
    available_balance: int = get_balance().json().get("balance")
    place_bet_cycles = available_balance // MAX_STAKE
    if place_bet_cycles > 0: # exhaust balance
        logger.info(f'Will execute {place_bet_cycles} to exhaust the balance')
        for _ in range(place_bet_cycles):
            matches = random.choice(matches)
            match_id = matches.get("id")
            place_bet(matchId=match_id, selection=valid_selections(), stake=MAX_STAKE)
    matches = random.choice(matches)
    match_id = matches.get("id")
    response = place_bet(matchId=match_id, selection=valid_selections(), stake=available_balance + 1 if available_balance else 1)
    check.equal(response.status_code, 422) # Transaction must be rejected as the balance can not cover the stake

# # TODO -> USD are returned in currency field, but the API documentation states that only EUR is supported
def test_place_bet_with_valid_mandatory_fields(get_matches, reset_balance, place_bet, valid_random_stakes) -> None:
    """Verify that only required fields are needed to place a bet."""
    reset_balance()
    matches = get_matches().json()
    assert matches, "Expected at least one upcoming match"
    random_match = random.choice(matches)
    match_id = random_match.get("id")
    odds_pairs = random_match.get("odds").items()
    selection, odds = random.choice(list(odds_pairs))
    stake = valid_random_stakes()
    response = place_bet(matchId=match_id, selection=selection.upper(), stake=stake)
    check.equal(response.status_code, 200)
    response_body = response.json()
    assert isinstance(response_body, dict), "Expected response body to be a dictionary"
    for field in expected_success_fields: check.is_in(field, response_body)

    check.equal(response_body.get("message"), "Bet placed successfully")
    check.equal(response_body.get("matchId"), match_id, f"Expected matchId in response to match the requested matchId: {match_id}")
    check.equal(response_body.get("selection"), selection.upper(), f"Expected selection in response to match the requested selection: {selection.upper()}")
    check.equal(response_body.get("stake"), stake, f"Expected stake in response to match the requested stake: {stake}")
    check.equal(response_body.get("odds"), odds, f"Expected odds in response to match the requested odds: {odds}")
    check.equal(response_body.get("payout"), round(stake * odds, 2), f"Expected payout in response to match the calculated payout: {stake * odds}")
    check.is_instance(response_body.get("balance"), (int, float), f"Expected balance in response to be numeric: {response_body.get('balance')}")
    check.equal(response_body.get("currency"), 'EUR', f"Expected default currency in response, got: {response_body.get('currency')}")


def test_place_bet_extract_stake_from_user_balance(get_matches, reset_balance, get_balance, place_bet, valid_random_stakes) -> None:
    """Verify that the stake once succesfully placed is extracted form the balance"""
    reset_balance()
    matches = get_matches().json()
    available_balance: int = get_balance().json().get("balance") 
    assert matches, "Expected at least one available match"
    random_match = random.choice(matches)
    match_id = random_match.get("id")
    odds_pairs = random_match.get("odds").items()
    selection, odds = random.choice(list(odds_pairs))
    stake = choose_stake(available_balance)
    response = place_bet(matchId=match_id, selection=selection.upper(), stake=stake)
    check.equal(response.status_code, 200)
    response_body = response.json()
    expected_remaining_balance = available_balance - stake
    actual_balance = response_body.get('balance')
    actual_payout = response_body.get('payout')
    expected_payout = round(odds*stake, 2)
    assert expected_remaining_balance == actual_balance, f'Remaining balance must be {expected_remaining_balance} instead it is {actual_balance}'
    assert expected_payout == actual_payout, f'Payout must be {expected_payout}, but is {actual_payout}'
