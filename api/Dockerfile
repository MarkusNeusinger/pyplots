# Dockerfile for pyplots FastAPI backend on Cloud Run
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY pyproject.toml .
COPY README.md .

# Install Python dependencies (production only, no test extras)
RUN pip install --no-cache-dir uv && \
    uv sync

# Copy application code
COPY api/ ./api/
COPY core/ ./core/

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port 8000 for FastAPI
EXPOSE 8000

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1

# Run FastAPI app with uvicorn
# Cloud Run provides PORT env var, default to 8000
CMD .venv/bin/uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}
