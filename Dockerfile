# Node stage — compile Tailwind CSS
FROM node:20-alpine AS assets
WORKDIR /app
COPY package.json package-lock.json* tailwind.config.js ./
COPY static/src ./static/src
COPY templates ./templates
RUN npm install && npm run build:css

# Python runtime
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY --from=assets /app/static/css ./static/css

# Vendor JS locally (no CDN dependency in production)
RUN mkdir -p static/vendor \
    && curl -fsSL https://unpkg.com/htmx.org@2.0.4/dist/htmx.min.js -o static/vendor/htmx.min.js \
    && curl -fsSL https://unpkg.com/alpinejs@3.14.8/dist/cdn.min.js -o static/vendor/alpine.min.js

RUN chmod +x deploy/entrypoint.sh

EXPOSE 8000

CMD ["/app/deploy/entrypoint.sh"]
