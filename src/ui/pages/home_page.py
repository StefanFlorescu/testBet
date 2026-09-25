"""Page object for the application home page and bet slip."""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from src.ui.pages.abstract_page import AbstractPage, Locator
import random

class HomePage(AbstractPage):
    """Expose all interactions with the application home page."""

    expected_title = "Sports Betting QA"
    _match_items = Locator(By.XPATH, '//div[@class="matchList"]/div[@class="card matchCard"]')
    _match_count = Locator(By.ID, "match-list-count")
    _bet_slip_teams = Locator(By.CSS_SELECTOR, "#bet-slip .betSelectionTeams")
    _bet_slip_market = Locator(By.CSS_SELECTOR, "#bet-slip .betSelectionMarket")
    _bet_slip_odds = Locator(By.CSS_SELECTOR, "#bet-slip .betSelectionOdds")
    _stake_input = Locator(By.ID, "bet-slip-stake-input")
    _total_stake = Locator(By.ID, "bet-slip-total-stake")
    _potential_payout = Locator(By.XPATH, '//span[@id="bet-slip-potential-payout"]')
    _place_bet = Locator(By.ID, "bet-slip-place-bet")
    _user_balance = Locator(By.ID, "bet-slip-balance")
    _success_modal = Locator(By.XPATH, '//div[@id="modal-success" and @role="dialog"]')

    def __init__(self, browser: WebDriver) -> None:
        super().__init__(browser)

    def open(self, url: str) -> None:
        """Open the application home page."""
        self._browser.get(url)
        _, _ = self._user_balance.first, self._match_items.all
    

    @property
    def match_items(self) -> list[WebElement]:
        """Return all currently displayed match cards."""
        return self._match_items.all

    @property
    def match_count(self) -> int:
        """Return the displayed match-count text."""
        text = self._match_count.first.text
        number = int("".join(filter(str.isdigit, text)))
        return number

    def select_random_odd(self) -> float:
        """Select one outcome for a match."""
        match = random.choice(self.match_items)
        odd_elem = match.find_element(By.XPATH, './/span[@class="oddsButtonValue"]')
        odd_value = float(odd_elem.text)
        odd_elem.click()
        self._browser.implicitly_wait(1)
        return odd_value

    @property
    def total_stake(self) -> str:
        """Return the displayed total stake."""
        # return float("".join(filter(str.isdigit, self._total_stake.first.text)))
        _text = self._total_stake.first.text
        return _text

    @property
    def potential_payout(self) -> str:
        """Return the displayed potential payout."""
        # return float("".join(filter(str.isdigit, self._potential_payout.first.text)))
        _text = self._potential_payout.first.text
        return _text

    @property
    def place_bet_enabled(self) -> bool:
        """Return whether the place-bet control is enabled."""
        return self._place_bet.first.is_enabled()

    def enter_stake(self, stake: str) -> None:
        """Replace the current stake with the supplied value."""
        input_element = self._stake_input.first
        input_element.clear()
        input_element.send_keys(stake)

    def place_bet(self) -> None:
        """Submit the selected bet."""
        self._place_bet.first.click()
    
    @property
    def success_modal_is_visible(self) -> bool:
        return self._success_modal.first.is_displayed()
