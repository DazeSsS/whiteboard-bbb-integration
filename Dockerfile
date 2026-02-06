FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
# USER appuser

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

COPY pyproject.toml uv.lock ./

RUN uv sync --no-dev --frozen

ENV PATH="/app/.venv/bin:$PATH"

COPY src/ ./src/
COPY alembic.ini ./

EXPOSE 8000
