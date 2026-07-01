# ---------------------------------------------------------
# Build Stage - Highly Optimized Environment Dependency Isolation
# ---------------------------------------------------------
FROM ghcr.io/astral-sh/uv:python3.12-alpine AS builder

WORKDIR /app

# Exclude unnecessary file copying by specifically mapping files first
COPY pyproject.toml uv.lock ./

# Mount the cached dependencies to optimize incremental builds
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# ---------------------------------------------------------
# Production Runtime Stage - Lightweight Container
# ---------------------------------------------------------
FROM python:3.12-alpine

WORKDIR /app

# Ensure standard output/error stream streams unbuffered
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Retrieve dependencies compiled during build stage
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy internal modular codebase
COPY main.py ./
COPY modules/ ./modules/
COPY memory/ ./memory/
COPY templates/ ./templates/
COPY tools/ ./tools/

# Establish running permissions
RUN adduser -D ecovibe && \
    chown -R ecovibe:ecovibe /app

USER ecovibe

EXPOSE 8080

# Start production server bound to target Cloud Run variables
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT}