FROM seleniarm/standalone-chromium:latest

USER root

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_CACHE_DIR=/tmp/uv-cache \
    UV_PYTHON_INSTALL_DIR=/opt/uv-python \
    LOG_LEVEL=INFO

WORKDIR /app

# us install for deps management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
RUN uv python install 3.14 \
    && chmod -R a+rX /opt/uv-python
# init environment
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --python 3.14


COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh \
    && mkdir -p "${UV_CACHE_DIR}" \
    && chown -R 1200:1200 /app "${UV_CACHE_DIR}"
# copy project needed sources
COPY src ./src
COPY tests ./tests
# change to regular user
USER 1200

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["uv", "run", "pytest", "--headed", "-v", "-m", "ui and api"]
