# Beamo Automated Testing Platform Dockerfile
FROM mcr.microsoft.com/playwright/python:v1.40.0-focal

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONPATH=/app
ENV BEAMO_ENV=dev
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install --with-deps

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p reports/{dev,stage,live}/{screenshots,videos,har}

# Create non-root user for security
RUN useradd -m -u 1000 testuser && \
    chown -R testuser:testuser /app
USER testuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import playwright; print('Playwright is available')" || exit 1

# Default command
CMD ["python", "run_tests.py", "--env", "dev", "--tags", "smoke"]
