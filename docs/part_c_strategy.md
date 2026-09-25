# Part C — Strategy & Recommendations

## 1. Automation strategy

The automation strategy prioritizes scenarios that can create financial loss,
invalid account state, incorrect transaction history or user being unable to properly use the system. 
In the context of a betting flow, the most valuable automated checks are not simply the easiest UI checks; 
They are the checks that safeguard transaction boundaries across both the frontend and backend. 

The two highest-risk documented defects identified and described in `docs/part_a_test_plan.md` are:

- **BUG-UI-003 — Bets can continue after the balance is exhausted**
  - The UI does not reliably reflect the remaining balance.
  - Additional bets can be placed after the actual balance has been exhausted.
  - The API accepts unaffordable bets and the balance can become negative.
  - This violates a fundamental financial rule and can create invalid account
    data.
- **BUG-UI-004 — Repeated clicks create multiple successful stakes**
  - A single intended action can generate multiple successful requests and
    multiple bets.
  - This can charge the user more than once and reduce the balance
    unexpectedly.
  - It indicates a need for duplicate-submission protection, idempotency, and
    transactional safeguards.

These defects were prioritized over the other documented findings because
BUG-UI-002 primarily concerns an incorrect UI payout and a stale displayed balance. In
BUG-UI-002, the successful API response contains the correct payout and
remaining balance. BUG-UI-003 and BUG-UI-004 can instead create invalid or
duplicate financial transactions. The API findings also demonstrate the need for consistent validation across the UI and backend. 

## 2. Why these tests were selected for automation

### UI test — critical single-bet placement journey

The Selenium UI test covers the main user journey:

1. Open the application with an authenticated user.
2. Select a match outcome.
3. Enter a valid stake.
4. Submit the bet.
5. Verify the success receipt and transaction values.

This test was selected because it pin-points that the UI does not 
updates its state correctly after the underlying API events are triggered

It also provides a starting point for extending coverage around BUG-UI-003 and
BUG-UI-004 since they follow the same user journey.
the same user journey can later be parameterized for an exhausted
balance and repeated-submit behavior. 

### API test — reject a stake greater than the available balance

The API test exhausts or accounts for the available balance and then attempts
to place an additional stake. It expects the API to reject the transaction
with a validation error.

This test was selected because balance enforcement is a server-side financial
validation. It must not depend on the frontend being correct or on a browser
being used. Testing it directly through the API makes the check faster,
deterministic, and capable of detecting the core risk behind BUG-UI-003,
including cases where the UI is stale or intentionally bypassed.


## 3. What remains manual or exploratory

Not every scenario should be automated immediately. 
Most of the critical bugs identified during the first hour were discovered through exploratory testing.
The following areas remain manual or exploratory until their behavior and requirements are stable:

- **Duplicate-submission investigation (BUG-UI-004):** repeated clicks,
  request timing, and concurrent requests are useful exploratory checks while
  the expected idempotency behavior and backend transaction model are being
  clarified. Once the expected behavior is agreed, this should become a
  deterministic API and UI regression test.
- **Visual and usability checks:** layout, spacing, responsive behavior,
  readability of validation messages, modal presentation, and the clarity of
  empty-filter states are better assessed manually.
- **Exploratory filtering:** combinations of date and odds filters are useful
  for discovering stale selections, misleading counts, and unexpected empty
  states. The current filtering defects were identified through exploratory testing.
- **Cross-browser and accessibility review:** Although the assignment currently focuses on desktop Chrome,
  keyboard navigation, focus behavior, screen-reader semantics, browser-specific rendering, and responsive
  layouts require broader test environments than the current one.
- **One-off defect reproduction:** exploratory checks used to investigate
  BUG-UI-001, BUG-UI-002, and BUG-UI-004 should remain manual until each
  expected result is expressed as a stable, repeatable contract.

Manual testing is not a replacement for the automated checks. It cis actually the basis that we start testing
Most critical bugs and high-risk user journeys become evident during thorough exploratory or smoke testing.
Automation complements manual testing by identifying scenarios that are extreme, rare, or difficult to reproduce
in normal day-to-day system usage. Normally, you should first use the target system as 
a normal user would under common usage patterns, and then start writing automated steps.

## 4. Recommendations for scaling the project

### 4.1 Add CI/CD stages with risk-based test suites

Run the suites in separate pipeline stages:

1. API smoke and authentication checks on every pull request.
2. API business-rule and contract tests on every pull request.
3. Critical UI smoke tests after the application is deployed to a test
   environment.
4. The broader UI/API regression suite on a scheduled run or before release.

Publish the `pytest-html` report and, when needed, `debug.log` as CI artifacts. 
This would keep defect trace and makes failures traceable to a specific build.

### 4.2 Data isolation and deterministic test state for parallel test runs

Use dedicated test users or a resettable test account for each test. Avoid
sharing mutable balance state between tests, and replace random selections
with seeded or explicitly selected match data where deterministic assertions
are required. Expose reset operations through pytest fixtures so tests do not depend on the underlying setup details.
This keeps test functions independent of the reset implementation.

For parallel execution, group tests and provision isolated users or isolated backend data instances.
This prevents one test from changing the balance or selections used by another test.

### 4.3 Define and enforce the financial contract at the API boundary

The API contract should explicitly define:

- the accepted currency and whether it is always `EUR`;
- minimum, maximum, decimal precision, and invalid stake validation messages;
- whether the balance check is atomic with bet creation transactions;
- the response and balance behavior after a successful bet;
- idempotency requirements for repeated submissions;
- handling of duplicate or concurrent requests, especially for financial transactions;
- kickoff-date timezone and “future” semantics.


## 5. Suggested next automation layers

After the current API and UI critical issues are addressed, the next useful layers
would be:

- API contract tests generated from the OpenAPI definition.
Schemathesis is already included in the project, but the OpenAPI document should first be complete and accurate. The current contract-testing entry point is at `tests/api/test_schema_validation.py`. We can include it in the test run once we have OpenApi propery configured.
- more service-level tests for balance deduction, atomicity, and idempotency since we indetified this to be a major defect;
- deterministic test-data builders for matches, odds, users, and balances;
- parameterized boundary tests for stake values and payout rounding. Already done partialy, but it is worth encapuslating then into dedicated fixtures;
- accessibility checks for the bet slip, validation messages, and receipt;
- visual regression checks for the receipt and empty-filter states;
- parallel CI execution with separate workers and isolated test data. For this I either need to be provided with more users or more separeted instances
