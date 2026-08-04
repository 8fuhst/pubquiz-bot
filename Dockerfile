FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim AS BASE

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .

RUN uv sync --locked --no-install-project

COPY . .

RUN uv sync --locked

CMD ["uv", "run", "--env-file", ".env", "bot.py"]