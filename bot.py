import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
    ConversationHandler
)
from flask import Flask, request
import config
from koyeb_api import KoyebAPI
import json
import os

# States
ACCOUNT_CHOICE, APP_CHOICE, ACTION_CHOICE = range(3)

# Initialize
app = Flask(__name__)
updater = None
logger = logging.getLogger(__name__)

def auth_check(func):
    def wrapper(update: Update, context: CallbackContext):
        if update.effective_user.id not in config.AUTHORIZED_USERS:
            update.message.reply_text("⛔ Unauthorized access!")
            return ConversationHandler.END
        return func(update, context)
    return wrapper

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(), updater.bot)
    updater.dispatcher.process_update(update)
    return "OK"

@auth_check
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton(acc, callback_data=f"acc_{acc}")]
        for acc in config.KOYEB_ACCOUNTS
    ]
    update.message.reply_text(
        "🔧 Select Koyeb Account:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return ACCOUNT_CHOICE

def account_choice(update: Update, context: CallbackContext):
    query = update.callback_query
    account_name = query.data.split("_")[1]
    context.user_data["account"] = account_name
    
    # Get apps
    api = KoyebAPI(config.KOYEB_ACCOUNTS[account_name])
    apps = api.get_apps()
    
    keyboard = [
        [InlineKeyboardButton(app["name"], callback_data=f"app_{app['id']}")]
        for app in apps
    ]
    query.edit_message_text(
        f"📦 Account: {account_name}\nSelect App:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return APP_CHOICE

def app_choice(update: Update, context: CallbackContext):
    query = update.callback_query
    app_id = query.data.split("_")[1]
    context.user_data["app_id"] = app_id
    
    keyboard = [
        [
            InlineKeyboardButton("📜 Logs", callback_data="act_logs"),
            InlineKeyboardButton("🔄 Restart", callback_data="act_restart")
        ],
        [
            InlineKeyboardButton("⏹ Stop", callback_data="act_stop"),
            InlineKeyboardButton("🚀 Redeploy", callback_data="act_redeploy")
        ]
    ]
    query.edit_message_text(
        f"⚙️ App ID: {app_id}\nChoose Action:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return ACTION_CHOICE

def action_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    action = query.data.split("_")[1]
    
    account = context.user_data["account"]
    app_id = context.user_data["app_id"]
    api = KoyebAPI(config.KOYEB_ACCOUNTS[account])
    
    if action == "logs":
        logs = api.get_logs(app_id)
        query.edit_message_text(f"📄 Logs for {app_id}:\n{logs}")
    else:
        success = api.app_action(app_id, action)
        status = "✅ Success" if success else "❌ Failed"
        query.edit_message_text(f"{status} performing {action} on {app_id}")
    
    return ConversationHandler.END

def main():
    global updater
    
    # Init Telegram
    updater = Updater(config.TELEGRAM_BOT_TOKEN)
    updater.bot.set_webhook(config.WEBHOOK_URL)
    
    # Conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ACCOUNT_CHOICE: [CallbackQueryHandler(account_choice)],
            APP_CHOICE: [CallbackQueryHandler(app_choice)],
            ACTION_CHOICE: [CallbackQueryHandler(action_handler)]
        },
        fallbacks=[]
    )
    
    updater.dispatcher.add_handler(conv_handler)
    
    # Start Flask
    app.run(host="0.0.0.0", port=config.PORT)

if __name__ == "__main__":
    main()
