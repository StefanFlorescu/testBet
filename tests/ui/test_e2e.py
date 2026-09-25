"""Smoke tests for the application home page."""

import pytest
import random
from src.logger import get_logger

pytestmark = [pytest.mark.ui, pytest.mark.e2e]
logger = get_logger('test_homePage')


def test_homePage_has_expected_title(page_factory, web_url) -> None:
    """Verify that the application opens with the expected page title."""
    home_page = page_factory.home_page
    home_page.open(web_url)
    assert home_page.title == "Sports Betting QA"

def test_home_page_list_items_match_counter(page_factory, web_url) -> None:
    """Verify that the displayed match counter equals the number of match cards."""
    home_page = page_factory.home_page
    home_page.open(web_url)
    assert home_page.match_count == len(home_page.match_items), 'Counter must match the actual item list'
    
def test_stake_limits(page_factory, web_url) -> None:
    """Verify that stakes above and below the allowed limits trigger validation messages."""
    home_page = page_factory.home_page
    home_page.open(web_url)
    home_page.select_random_odd()
    home_page.enter_stake(1000)
    assert home_page.text_is_visible('Maximum stake is €100.00'), 'Max stake validation message is visible'
    home_page.enter_stake(0.1)
    assert home_page.text_is_visible('Minimum stake is €1.00'), 'Min stake validation message is visible'
    
def test_home_page_select_random_match(reset_balance_page_factory, web_url, valid_random_stakes) -> None:
    """Verify that selecting an odd and entering a valid stake updates the bet slip."""
    stake = valid_random_stakes()
    home_page = reset_balance_page_factory.home_page
    home_page.open(web_url)
    odd_selected = home_page.select_random_odd()
    expected_payout = round(stake*odd_selected, 2)
    home_page.enter_stake(stake)
    logger.info(f'Enter stake {stake} at odd {odd_selected}')
    assert str(expected_payout) in home_page.potential_payout, 'Computation odd*strake must match'
    assert str(stake) in home_page.total_stake, 'Input stake must be equal with total stake'
    assert home_page.place_bet_enabled, 'Place Bet button must be enabled'

# TODO -> report on the PayOut value diplayed on the success modal, it is not displayed properly compared to the the expected one
def test_home_page_place_stake(reset_balance_page_factory, web_url, valid_random_stakes) -> None:
    """Verify that placing a valid stake displays the success messages and the correct data in the confirmation modal."""
    stake = valid_random_stakes()
    home_page = reset_balance_page_factory.home_page
    home_page.open(web_url)
    odd_selected = home_page.select_random_odd()
    expected_payout = round(stake*odd_selected, 2)
    home_page.enter_stake(stake)
    logger.info(f'Enter stake {stake} at odd {odd_selected}')
    home_page.place_bet()
    assert home_page.success_modal_is_visible, "Success modal must be vizible"
    assert home_page.text_is_visible('Bet Placed Successfully!'), 'Success message is visible'
    assert home_page.text_is_visible(f'{odd_selected}'), 'Odds message is visible'
    assert home_page.text_is_visible(f'{stake}'), 'Placed stake message is visible'
    assert home_page.text_is_visible(f'{expected_payout}'), 'Payout message is visible'
