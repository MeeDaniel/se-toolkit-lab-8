# Multi-stage build for nanobot gateway
# Uses uv for fast, reproducible builds

# ---------------------------------------------------------------------------
# Stage 1: Builder
# ---------------------------------------------------------------------------
FROM astral/uv:python3.14-bookworm AS builder

WORKDIR /app

# Copy entire workspace from root context
COPY --from=workspace . /app/

# Install the nanobot package and its workspace dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --package nanobot --package nanobot-webchat

# ---------------------------------------------------------------------------
# Stage 2: Runtime
# ---------------------------------------------------------------------------
FROM python:3.14-slim AS runtime

WORKDIR /app

# Create non-root user for security
RUN groupadd --system --gid 999 nonroot && \
    useradd --system --uid 999 --gid 999 --create-home nonroot

# Copy virtual environment from builder
COPY --from=builder --chown=nonroot:nonroot /app/.venv /app/.venv

# Copy the entire workspace (needed for MCP server and webchat package)
COPY --from=builder --chown=nonroot:nonroot /app /app

# Set up PATH to use venv
ENV PATH="/app/.venv/bin:$PATH"

# Switch to non-root user
USER nonroot

# Default command runs the entrypoint
CMD ["python", "/app/nanobot/entrypoint.py"]
