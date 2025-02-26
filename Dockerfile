FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Environment variables (will be set in Koyeb dashboard)
ENV PORT=8080
EXPOSE 8080

# Run with production server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "bot:app"]
