import os

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
AUTHORIZED_USERS = [int(os.getenv("AUTHORIZED_USER_ID"))]  # Your Telegram ID

# Koyeb Webhook Configuration
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://your-koyeb-service-name.koyeb.app/webhook")
PORT = int(os.environ.get("PORT", 8080))

# Koyeb Accounts (Name: API Key)
KOYEB_ACCOUNTS = {
    "account-1": os.getenv("KOYEB_ACCOUNT_1"),
    "account-2": os.getenv("KOYEB_ACCOUNT_2")
}
