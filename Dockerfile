FROM python:3.14.6-slim-trixie AS BASE

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .

RUN uv sync

COPY . .

CMD ["uv", "run", "--env-file", ".env", "bot.py"]