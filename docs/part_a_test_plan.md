# Part A — Manual QA Test Plan

## 1. Objective and scope

This test plan covers the critical single-bet placement journey for the sports
betting application:

1. View available football matches.
2. Select a match and betting outcome.
3. Enter a stake in the bet slip.
4. Place the bet.
5. Verify the receipt, payout, and updated balance.

The plan focuses on the highest business and user risks identified in the
feature specification and the existing API tests. It intentionally contains
six focused scenarios rather than exhaustive coverage.

## 2. Test assumptions and preconditions

- The application is opened with a valid `user-id` query param.
- The tester has access to a user with a known balance as float number.
- The application is rendering in the latest desktop Chrome browser.
- At least one match is available for selection and it has the 3 distinct selections
- The monetary currency for displayed funds and transactions is EUR.
- The initial/reset balance is expected to be €125.50 unless the application
  or test data specifies otherwise.
- No execution result is inferred from this document. Actual observations and
  defects must be recorded after the scenarios are run.
- The MIX_STEAKE = 1, the MAX_STAKE = 100
- User balance is dispalyed
- Matches filter controls are also displayed

## 3. Prioritized scenarios

### TC-UI-001 — Place a valid single bet and verify the sucess receipt

- **Priority:** Critical
- **Risk rationale:** Bet placement is the primary business journey. An
  incorrect receipt, payout, or balance update can create a financial
  discrepancy even when the transaction appears successful.
- **Steps:**
  1. Open the application.
  2. Select an upcoming match from the available ones.
  3. Select one outcome: home win, draw, or away win.
  4. Confirm that the bet slip shows the selected match, outcome, and odds.
  5. Enter a valid stake between €1.00 and €100.00 that is within the
     available balance.
  6. Place the bet.
- **Expected result:**
  - The bet is accepted exactly once.
  - A success receipt is displayed.
  - The receipt contains the bet ID, match, selection, stake, odds, payout as odds*stake,
    and timestamp.
  - Each placed receipe must have an unique value
  - Receipt values match the selected match and values shown before placement.
  - Payout equals `stake × odds`, using the application’s documented rounding.
  - Currency is EUR.
  - The available balance decreases by exactly the stake amount after successful placement.

### TC-UI-002 — Reject a stake greater than the available balance

- **Priority:** Critical
- **Risk rationale:** Allowing an unaffordable stake can create an invalid
  financial transaction, a negative balance, or an inconsistent balance across
  the application. This risk is also flagged by the known API validation failed tests.
- **Steps:**
  1. Open the application.
  2. Record the current available balance.
  3. Select an upcoming match and one outcome.
  4. Enter a stake greater than the available balance.
  5. Attempt to place the bet.
- **Expected result:**
  - The bet is rejected.
  - A clear validation message states that the stake cannot exceed the
    available balance.
  - No success receipt is displayed.
  - No taransaction is allowed or generated ("Place bet" button inactive )
  - The balance remains unchanged.

### TC-UI-003 — Reject invalid and below-minimum stake values

- **Priority:** High
- **Risk rationale:** Invalid stake validation protects the financial boundary
  of the product. Negative-stake validation is already identified as an API
  risk and should be checked through the user interface as well.
- **Steps:**
  1. Select an upcoming match and one outcome.
  2. Enter a negative value and attempt to place the bet.
  3. Enter `€0.00` and attempt to place the bet.
  4. Enter `€0.99` and attempt to place the bet.
  5. Enter invalid value `ten` | empty string
- **Expected result:**
  - Negative, zero, and €0.99 values are rejected with an appropriate
    validation message.
  - No rejected attempt creates a receipt or changes the balance.
  - The "Place bet" button inactive

### TC-UI-004 — Verify maximum stake and decimal precision boundaries

- **Priority:** High
- **Risk rationale:** Boundary and rounding defects can cause users to place
  stakes outside the documented limits or produce incorrect payout values.
- **Steps:**
  1. Ensure the available balance is at least €100.00.
  2. Select an upcoming match and one outcome.
  3. Enter exactly €100.00 and place the bet.
  4. Reset the balance 
  5. Enter €100.01 and attempt to place the bet.
  6. Reset the balance or establish a fresh test state.
  7. Enter a valid two-decimal value such as €20.60 and place the bet.
- **Expected result:**
  - €100.00 is accepted when the balance covers it.
  - €100.01 is rejected with a maximum-stake validation message.
  - A valid two-decimal stake is accepted without unexpected truncation or
    rounding.
  - The receipt and balance calculations use the submitted monetary value.

### TC-UI-005 — Verify bet-slip stake, odds, and payout consistency

- **Priority:** High
- **Risk rationale:** Incorrect or inconsistent financial values in the bet slip
  can cause the user to submit a bet with an unintended stake or misunderstand
  the potential return. The stake and payout values must remain consistent
  from selection through placement.
- **Steps:**
  1. Select an available match and one betting outcome.
  2. Record the selected odds displayed for that outcome.
  3. Enter a valid stake amount and record the entered value.
  4. Review the bet slip fields for the selected odds, stake, `Total Stake`,
     and `Potential Payout`.
  5. Before placing the bet, change the stake to another valid value and
     review the calculated fields again.
- **Expected result:**
  - The odds shown in the bet slip equal the odds of the selected outcome.
  - The stake shown in the bet slip equals the value entered by the user.
  - `Total Stake` equals the entered stake.
  - `Potential Payout` equals `selected odds coeficiend × entered stake`.
  - Updating the stake recalculates `Total Stake` and `Potential Payout`
    immediately and accurately.
  - No field displays stale, truncated, or incorrectly rounded values.

### TC-UI-006 — Prevent duplicate submission and preserve post-bet state

- **Priority:** Medium
- **Risk rationale:** Duplicate submissions can charge a user twice for one
  intended bet. Incorrect post-submission state can also leave stale selections
  available for accidental reuse.
- **Steps:**
  1. Select an upcoming match and enter a valid stake.
  2. Click the "place bet" control.
  3. Immediately click the control again or press Enter again while the first
     request is processing.
  4. Observe the receipt, bet slip, and balance, network requests
- **Expected result:**
  - Exactly one bet is created.
  - The placement control is disabled or otherwise protected while the
    request is processing.
  - Exactly one receipt is displayed not multiple
  - The balance decreases once by the stake amount, not more
  - If there are any subsequent requests for the same stake they are blocked with the respective error messages

### TC-UI-007 — Filter matches by date range and odds range

- **Priority:** High
- **Risk rationale:** Incorrect match filtering can hide eligible betting
  opportunities or display matches outside the user’s requested criteria.
  Odds filtering must evaluate all three outcomes and include a match when at
  least one coefficient falls within the selected range.
- **Steps:**
  1. Record the kickoff date and home, draw, and away odds for the displayed
     matches.
  2. Set the `Date from` and `Date to` filters to a range containing a known
     subset of match dates.
  3. Apply the date filter.
  4. Verify that every displayed match has a kickoff date within the selected
     date range.
  5. Set the `Odds from` and `Odds to` filters to a range containing at least
     one known coefficient from a selected match.
  6. Apply the odds filter.
  7. Verify that every displayed match has at least one home, draw, or away
     coefficient within the selected odds range.
  8. Test boundary values (minimum so that no matches match the filters) using coefficients equal to the configured
     `Odds from` or `Odds to` values.
  9. Apply the date and odds filters together, then clear the filters.
- **Expected result:**
  - The date filter displays only matches whose kickoff dates are within the
    selected from-to range.
  - The odds filter includes a match when at least one of its three
    coefficients is within the selected odds range.
  - A match is excluded when none of its coefficients is within the selected
    odds range.
  - Boundary values are handled according to the documented inclusive filter
    behavior.
  - Applying both filters returns only matches satisfying both criteria.
  - Clearing the filters restores the complete available match list.

### TC-UI-008 — Allow one selection only and populate the bet slip automatically

- **Priority:** High
- **Risk rationale:** The product supports only one active bet at a time. If
  multiple odds can be selected or the bet slip is populated with the wrong
  match or coefficient, the user may submit a different bet from the one they
  intended.
- **Steps:**
  1. Open the match list and select one available match.
  2. Select exactly one odd coefficient for that match: home, draw, or away.
  3. Open or observe the bet slip.
  4. Verify the teams displayed in the bet slip against the selected match.
  5. Verify the selected coefficient against the coefficient on the selected
     outcome.
  6. Attempt to select a second odd for the same match.
  7. Attempt to select an odd from a different match, if another match is
     available.
- **Expected result:**
  - The user can select only one odd for one match.
  - The bet slip is populated automatically after the selection.
  - The bet slip displays the correct home and away team names for the
    selected match.
  - The bet slip displays the exact coefficient selected by the user.
  - Selecting another odd does not create multiple active selections or
    multiple bet-slip entries.
  - Selecting an odd from another match is blocked or replaces the existing
    selection according to the documented single-bet behavior; it must not
    leave more than one active selection.

## 4. Recommended execution order

Execute the following three scenarios first, as required by the assignment:

1. **TC-UI-001** — Valid bet placement and receipt verification
2. **TC-UI-002** — Stake greater than available balance
3. **TC-UI-003** — Invalid and below-minimum stake values

Together, these cover the core revenue flow and the two most important
financial validation risks. After execution, document the observed results and
any defects separately using the assignment’s required fields:

- Bug ID and title
- Severity
- Reproduction steps
- Expected versus actual result
- Business impact
- Evidence

## 5. Exploratory defects

### BUG-UI-001 — Empty filtered match list shows an incorrect count and retains a stale bet selection

- **Severity:** High
- **Reproduction steps:**
  1. Select an available match outcome and verify that the selected odd is
     displayed in the bet slip.
  2. Apply a date or odds filter combination that returns no matches.
  3. Observe the match-list page and the bet slip.
- **Expected result:**
  - The page clearly indicates that no matches satisfy the selected filters,
    for example, `No matches found`.
  - The displayed match count is `Showing 0 matches`.
  - The bet slip is cleared or the selected odd is marked unavailable because
    its match is no longer included in the filtered results.
  - The user cannot proceed with a stale selection that is hidden by the
    active filters.
- **Actual result:**
  - The match list is empty without an explanatory message.
  - The page still displays `Showing 103 matches`.
  - The bet slip continues to display the previously selected odd.
- **Business impact:** The UI presents contradictory information and allows a
  user to retain or potentially submit a bet for a match that is not present
  in the active filtered result set. This can lead to user confusion and an
  unintended bet.
- **Evidence:** artifacts/proof1.jpg

### BUG-UI-002 — Successful bet receipt shows an incorrect payout and stale balance

- **Severity:** Critical
- **Reproduction steps:**
  1. Select an available match and one valid odd.
  2. Enter a valid stake.
  3. Place the bet successfully.
  4. Compare the values displayed in the UI with the values returned in the
     successful `POST` response.
  5. Refresh the page and compare the displayed balance again.
- **Expected result:**
  - The success receipt displays the correct Bet ID, match name, stake, odds,
    and potential payout from the successful API response.
  - The potential payout equals the selected odds multiplied by the stake.
  - The available balance is immediately updated to the remaining balance
    after the stake is deducted.
  - The user can rely on the displayed balance without manually refreshing
    the page.
- **Actual result:**
  - The Bet ID, match name, stake, and odds are displayed correctly.
  - The potential payout displayed by the UI is incorrect.
  - The available balance is not refreshed to the correct remaining value
    after the bet is placed.
  - Refreshing the page is required before the correct balance is displayed.
  - The successful `POST` response contains the correct payout and remaining
    balance, so the UI has the data required to update these elements.
- **Business impact:** The stale balance is financially misleading. A user may
  continue placing bets believing that more funds are available than actually
  remain, which can result in rejected bets, inconsistent expectations, or
  unsafe betting decisions. The incorrect potential payout also undermines
  trust in the bet receipt.
- **Evidence:** artifacts/proof2.jpg (initial state), artifacts/proof3.jpg(after state)

### BUG-UI-003 — Bets can continue after the balance is exhausted, resulting in a negative user balance

- **Severity:** Critical
- **Reproduction steps:**
  1. Start with a user whose available balance is known.
  2. Place valid bets until the available balance is exhausted.
  3. Without refreshing the page, place another valid stake.
  4. Repeat the placement with another valid stake if the application still
     permits it.
  5. Refresh the page and inspect the resulting balance.
- **Expected result:**
  - After each successful bet, the displayed balance is updated immediately.
  - Once the remaining balance is insufficient for a stake, the bet is
    rejected.
  - The frontend prevents submission of a stake greater than the current
    available balance.
  - The API independently validates the balance and rejects unaffordable
    bets, even if the frontend state is stale or bypassed.
  - The user balance can never become negative.
- **Actual result:**
  - The UI does not show the updated remaining balance after bets are placed.
  - Additional stakes can be placed after the user’s actual balance has been
    exhausted.
  - The frontend does not prevent bets based on the actual remaining balance.
  - The API also accepts the additional unaffordable bets instead of
    rejecting them.
  - The balance can become negative.
- **Business impact:** This is a critical financial and data-integrity defect.
  It allows users to wager funds they do not have and produces an invalid
  negative account balance. The stale UI hides the risk, while the missing
  server-side validation allows the invalid transaction to be completed.
- **Evidence:** artifacts/proof4.jpg (API validation fails), artifacts/proof5.jpg(UI state)

### BUG-UI-004 — Repeated clicks on Place bet create multiple successful stakes

- **Severity:** Critical
- **Reproduction steps:**
  1. Select an available match and one valid odd.
  2. Enter a valid stake.
  3. Click the `Place bet` control multiple times in quick succession.
  4. Inspect the network activity and the resulting receipts, stakes, and
     balance.
- **Expected result:**
  - The first click submits one bet.
  - The `Place bet` control is disabled or otherwise protected while the
    request is processing.
  - Further clicks do not create additional bets or send additional
    successful POST requests.
  - Exactly one receipt is displayed and the balance is reduced once by the
    submitted stake.
- **Actual result:**
  - Multiple clicks create multiple stakes.
  - Multiple POST requests are sent and completed successfully.
  - More than one bet is created from a single intended user action.
- **Business impact:** This is a critical financial-integrity defect. A user
  can be charged multiple times unintentionally, lose more balance than
  expected, and receive multiple successful transactions for one intended bet.
  I suspect that the issue in this case is due to missing idempotency and concurrent-request protection on the BE side.
- **Evidence:** artifacts/proof6.jpg (API calls),
