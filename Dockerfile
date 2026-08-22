FROM python:3.11-slim

LABEL org.opencontainers.image.title="Hermes Agents Forge"
LABEL org.opencontainers.image.description="Hermes-native bootstrap repository for multi-profile agent teams"
LABEL org.opencontainers.image.authors="Julien Chevallier <juliench82@users.noreply.github.com>"
LABEL org.opencontainers.image.source="https://github.com/juliench82/hermes-agents-forge"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml .
COPY compiler/ ./compiler/
COPY runtime/ ./runtime/
COPY scripts/ ./scripts/
COPY schemas/ ./schemas/
COPY catalog/ ./catalog/
COPY shared/ ./shared/
COPY onboarding/ ./onboarding/
COPY skills/ ./skills/
COPY bootstrap.manifest.json .
COPY team-designer.yaml .
COPY onboarding-loop.yaml .

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Set environment
ENV HERMES_HOME=/root/.hermes
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["python", "-m", "compiler", "--help"]
