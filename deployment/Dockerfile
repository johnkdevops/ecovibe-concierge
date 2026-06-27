FROM python:3.12-slim

WORKDIR /app

# Copy requirements and install
COPY pyproject.toml .
COPY uv.lock* .  # if you have one
RUN pip install uv && uv sync --frozen

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Run with uvicorn (FastAPI)
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]