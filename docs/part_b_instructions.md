# Part B — Automation

## 1. Automation approach

The project uses Python, `pytest`, `uv`, `requests`, and Selenium WebDriver.
The tests are split into API and UI layers:

- **API tests** validate HTTP status codes, authentication, response payloads,
  business rules, and response schemas.
- **UI tests** use Selenium and page objects to validate the most important
  user flows in the web application.

The API and UI tests share configuration and pytest fixtures. The application
URLs and user identity are read from environment variables through
`src/config.py`; local secrets are kept in `.env`, which is not committed.
Use please the .env.example as a template for your own .env file, 
also you can opt to inject the required environment variables throug other methods.

## 2. Project structure

```text
.
├── Dockerfile
├── docker-entrypoint.sh
├── pyproject.toml
├── uv.lock
├── .env.example
├── src/
│   ├── api/
│   │   └── client.py
│   ├── config.py
│   ├── logger.py
│   └── ui/
│       ├── page_factory.py
│       └── pages/
│           ├── abstract_page.py
│           └── home_page.py
├── tests/
│   ├── conftest.py
│   ├── api/
│   │   └── test_*.py
│   └── ui/
│       ├── conftest.py
│       └── test_*.py
└── docs/
    └── *.md
```

### Source code description

- `src/config.py` defines typed settings loaded from `.env`.
- `src/logger.py` configures test logging.
- `src/api/client.py` contains the reusable HTTP client used by API fixtures.
- `src/ui/pages/abstract_page.py` contains shared Selenium page functionality,
  explicit visibility waits, and the `Locator` descriptor.
- `src/ui/pages/home_page.py` contains the Home Page object, including the
  bet-slip interactions. The bet slip is intentionally kept as part of the
  home page object because it is displayed on the same application page.
- `src/ui/page_factory.py` creates page objects for tests without requiring
  tests to construct concrete page classes directly.

### Test support

- `tests/conftest.py` contains shared API fixtures, application URLs, logging
  setup, and the `--headed` pytest option meant for UI test, if ommited then it will default to false.
- `tests/ui/conftest.py` creates and closes a Chrome WebDriver instance and
  exposes the page-object factory.
- `src/api/client.py` and the fixtures provide authenticated and unauthenticated
  request sessions as required by each API scenario.

## 3. Tests implemented so far

### API tests

The API suite currently covers:

- health and service availability;
- retrieving matches and validating required match fields;
- validating kickoff-date format and date rules;
- validating HOME, DRAW, and AWAY odds;
- retrieving the authenticated balance;
- validating balance fields, currency, numeric type, and non-negative values;
- resetting the balance;
- placing valid bets;
- invalid stake values and invalid match identifiers;
- unauthorized access check to protected endpoints;
- ...

Some schema and exploratory scenarios are marked `demo` or skipped while they
are still being developed.

### UI tests

The Selenium suite currently covers:

- opening the application and verifying the page title;
- verifying that the displayed match counter equals the number of match cards;
- validating minimum and maximum stake messages;
- selecting a random match outcome;
- entering a valid stake and checking bet-slip stake, odds, payout, and button
  state;
- placing a valid bet and checking the confirmation modal.

UI tests use the `HomePage` page object and explicit visibility waits instead of
direct Selenium interactions in the test functions.

## Execution options for tests:

### 4. Local execution with `uv`

The host machine must have Python 3.14 and `uv` installed. From the repository
root:

1. Create a local environment file and set the needed vars in it:

   ```bash
   cp .env.example .env
   ```

2. Synchronize the locked dependencies:

   ```bash
   uv sync
   ```

3. Run both the API and UI test suites:

   ```bash
   uv run pytest -v -m "ui or api"
   ```

4. Run only the UI tests with a visible browser:

   ```bash
   uv run pytest --headed -v -m ui
   ```

5. Run only the API tests:

   ```bash
   uv run pytest -v -m api
   ```

Without `--headed`, the UI fixture runs Chrome in headless mode. API tests do
not take this command line flag into account.

### 5. Docker execution

The Docker image is based on
`seleniarm/standalone-chromium`. It provides Chromium, ChromeDriver, Xvfb,
VNC, and noVNC. uv, Python 3.14 and the project dependencies are installed with
`uv` during the image build.

Build the image:

```bash
docker build -t testbet-tests .
```

Run the default API and UI command:

```bash
docker run --rm --env-file .env testbet-tests
```

The default Docker command is:

```bash
uv run pytest --headed -v -m "ui or api"
```

The entrypoint starts the Selenium display and browser services before
executing pytest(docker-entrypoint.sh). The `--env-file .env` option supplies the application URLs
and user ID without copying secrets into the image.

But of course you can run our own pytest command, so any pytest
selection can be run without rebuilding the image:

```bash
docker run --rm --env-file .env testbet-tests \
  uv run pytest --headed -v -m api

docker run --rm --env-file .env testbet-tests \
  uv run pytest --headed -v -m ui

docker run --rm --env-file .env testbet-tests \
  uv run pytest --headed -v tests/api/test_place_bet.py
```

## 6. Pytest markers

Markers are declared in `pyproject.toml` and can be combined with `and`, `or`,
and `not`. Make your own selections if you want to following the pytest marker guidelines.
Examples:

```bash
# All API tests
uv run pytest -v -m api

# API tests for matches only
uv run pytest -v -m "api and matches"

# API tests except access tests
uv run pytest -v -m "api and not access"

# UI end-to-end tests
uv run pytest --headed -v -m "ui and e2e"

# API and UI tests together
uv run pytest -v -m "api or ui"
```

The same marker expressions work in Docker:

```bash
docker run --rm --env-file .env testbet-tests \
  uv run pytest --headed -v -m "api and bets"
```


## 7. Selecting tests by file or test name

Pytest also supports selecting tests by path:

```bash
# Entire API directory
uv run pytest -v tests/api

# Entire UI directory
uv run pytest --headed -v tests/ui

# One test module
uv run pytest -v tests/api/test_balance.py

# One test function
uv run pytest -v tests/api/test_balance.py::test_get_balance_endpoint_returns_success

# Tests whose names contain "stake"
uv run pytest --headed -v -k stake
```

Path and marker filters can be combined:

```bash
uv run pytest --headed -v tests/ui -m e2e -k place
```

Before execution, available tests and their markers can be inspected with:

```bash
uv run pytest --collect-only -q
```

## 8. Generating HTML reports

The `pytest-html` plugin can generate a report for any test selection. The
`--self-contained-html` option embeds the report assets in the HTML file.
Please note the `reports` folder is. gitignored.

### Local execution with `uv`

Create the report directory and run the tests:

```bash
mkdir -p reports
uv run pytest -v -m "api or ui" \
  --html=reports/test-report.html \
  --self-contained-html
```

Reports for individual test groups can be generated in the same way:

```bash
uv run pytest -v -m api \
  --html=reports/api-report.html \
  --self-contained-html

uv run pytest --headed -v -m ui \
  --html=reports/ui-report.html \
  --self-contained-html
```

### Docker execution

Mount the local `reports/` directory into the container so the generated file
remains available after the container exits:

```bash
mkdir -p reports
docker run --rm \
  --env-file .env \
  -v "$PWD/reports:/app/reports" \
  testbet-tests \
  uv run pytest --headed -v -m "api or ui" \
  --html=reports/test-report.html \
  --self-contained-html
```

The report is written to `reports/test-report.html` on the host.

## 9. Current Test Output

The test suite currently contains failing scenarios that expose defects in the
test target platform. These failures are intentional test results, not automation
framework failures. The related `TODO` comments in the test files identify the
known defects:

- **Matches API:** returned `kickoffDate` values are not consistently in the
  future, although the API contract requires upcoming matches with respect to the current date.
- **Place-bet API:** negative stake values miss validation and the
  transaction is accepted by the API.
- **Place-bet API:** stake validation does not prevent placing a bet greater
  than the current available user balance.
- **Place-bet API:** the successful response returns `USD` in the currency
  field, although the API documentation and test contract require `EUR`.
- **UI:** the payout displayed in the successful-bet confirmation modal does
  not match the expected stake multiplied by the selected odds.

Run the relevant tests to observe these results:

```bash
uv run pytest -v -m "api or ui"
```
