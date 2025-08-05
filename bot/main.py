from pyrogram import Client
from bot.config import API_ID, API_HASH, BOT_TOKEN
from bot.handlers import start, account, admin  # Add more as you finish

app = Client(
    name="sh_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Initialize handlers
start.init(app)
account.init(app)
admin.init(app)
# Add other handlers like: cap.init(app), support.init(app), withdraw.init(app)

if __name__ == "__main__":
    print("✅ Bot is starting...")
    app.run()