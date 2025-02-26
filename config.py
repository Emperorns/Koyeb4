import os

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_BOT_TOKEN")
AUTHORIZED_USERS = [123456789]  # Your Telegram User ID

# Webhook
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://your-domain.com/webhook")
PORT = int(os.environ.get("PORT", 5000))

# Koyeb Accounts (Name: API Key)
KOYEB_ACCOUNTS = {
    "my-account-1": os.getenv("KOYEB_ACCOUNT_1"),
    "my-account-2": os.getenv("KOYEB_ACCOUNT_2")
}
