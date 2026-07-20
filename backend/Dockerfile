FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    libpango-1.0-0 libpangoft2-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# torch alone is ~195MB, and pip's 15s default socket timeout makes this layer fail
# on an ordinary connection hiccup. A failed build leaves the previously built
# image in place, so the stack silently keeps serving stale code — be patient here
# instead.
RUN pip install --no-cache-dir --default-timeout=180 --retries 10 -r requirements.txt

COPY . .
RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
