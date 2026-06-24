FROM node:22-bookworm AS builder

WORKDIR /app

COPY package.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile

COPY . .
RUN pnpm build

FROM python:3.13-slim-bookworm AS runtime

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    libgbm-dev \
    libnss3 \
    libasound2 \
    libxshmfence1 \
    libglib2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libpango-1.0-0 \
    libcairo2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libdrm2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir \
    django \
    python-dotenv \
    apscheduler \
    requests \
    playwright \
    openai \
    django-cf \
    django-browser-reload \
    django-pwa \
    gunicorn

RUN python -m playwright install chromium \
    && python -m playwright install-deps chromium

COPY --from=builder /app .

RUN python3 manage.py collectstatic --noinput
EXPOSE 8000
CMD ["gunicorn", "-c", "gunicorn.conf.py"]