FROM python:3.10-slim-bookworm as BASE

WORKDIR /app

COPY requirements.txt .

RUN pip install -y --no-install-recommends --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "bot.py"]