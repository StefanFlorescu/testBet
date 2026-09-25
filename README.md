Look for the docs/*.pdf files to understand the context of the assignemtn
BASE_URL of the application: https://qae-assignment-tau.vercel.app/?
API DOCUMENTATION URL: https://qae-assignment-tau.vercel.app/api/docs

## Run tests in Docker

Build the test image:

```bash
docker build -t testbet-tests .
```

Run the demo UI tests using the Chromium and display services provided by
`seleniarm/standalone-chromium`:

```bash
docker run --rm --env-file .env testbet-tests
```

The container runs this command by default:

```bash
LOG_LEVEL=INFO uv run pytest --headed -m demo
```

The image installs Python 3.14 with `uv`, because the base Selenium image
provides the browser services but does not provide the Python version required
by this project.

The default command can be overridden after the image name. For example, run
tests selected by another marker:

```bash
docker run --rm --env-file .env testbet-tests \
  uv run pytest --headed -m api

docker run --rm --env-file .env testbet-tests \
  uv run pytest --headed -m "ui and not demo"
```

You can also pass any normal pytest arguments:

```bash
docker run --rm --env-file .env testbet-tests \
  uv run pytest --headed tests/ui/test_e2e.py -k place_stake
```

The entrypoint starts the Selenium services and then executes the command
supplied after the image name. If no command is supplied, Docker uses the
default `demo` command from `CMD`.
