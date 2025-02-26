# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY config.py .
COPY koyeb_api.py .
COPY bot.py .

# Environment variables (override these when deploying)
ENV TELEGRAM_TOKEN="your_bot_token"
ENV WEBHOOK_URL="https://your-domain.com/webhook"
ENV PORT=5000

# Expose webhook port
EXPOSE $PORT

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "--workers", "2", "bot:app"]
