"""Smoke tests for the application home page."""

import pytest
import random
from src.logger import get_logger

pytestmark = [pytest.mark.ui, pytest.mark.access, pytest.mark.demo]
logger = get_logger('test_homePage')


def test_homePage_has_expected_title(page_factory, web_url) -> None:
    """Verify that the application opens with the expected page title."""
    home_page = page_factory.home_page
    home_page.open(web_url)
    assert home_page.title == "Sports Betting QA"


def test_home_page_list_items_match_counter(page_factory, web_url) -> None:
    home_page = page_factory.home_page
    home_page.open(web_url)
    assert home_page.match_count == len(home_page.match_items), 'Counter must match the actual item list'
    
def test_home_page_select_random_match(page_factory, web_url, valid_random_stakes) -> None:
    stake = valid_random_stakes()
    home_page = page_factory.home_page
    home_page.open(web_url)
    odd_selected = home_page.select_random_odd()
    expected_payout = round(stake*odd_selected, 2)
    home_page.enter_stake(stake)
    logger.info(f'Enter stake {stake} at odd {odd_selected}')
    assert str(expected_payout) in home_page.potential_payout, 'Computation odd*strake must match'
    assert str(stake) in home_page.total_stake, 'Input stake must be equal with total stake'
    assert home_page.place_bet_enabled, 'Place Bet button must be enabled'
    
    
    