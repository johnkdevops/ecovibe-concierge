# ---------------------------------------------------------
# Build Stage - Highly Optimized Debian-Slim Base (Native glibc)
# ---------------------------------------------------------
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

WORKDIR /app

# Purge any leaked Windows PATH variables containing drive colons (e.g., C:\...)
# and hard-reset to clean, standard Linux environment paths.
ENV PATH="/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin"

# Copy pyproject.toml and optionally uv.lock if present using a wildcard hack.
# This prevents Docker from crashing the build if uv.lock is not yet generated locally!
COPY pyproject.toml uv.loc[k] ./

# Mount the cached dependencies to optimize incremental builds
RUN uv sync --no-install-project --no-dev

# ---------------------------------------------------------
# Production Runtime Stage - Lightweight Container
# ---------------------------------------------------------
FROM python:3.12-slim-bookworm

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

# Establish secure non-root running permissions
RUN useradd -u 10001 ecovibe && \
    chown -R ecovibe:ecovibe /app

USER ecovibe

EXPOSE 8080

# Start production server bound to target Cloud Run variables
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT}