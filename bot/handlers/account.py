# bot/handlers/account.py

from pyrogram import Client, filters
from pyrogram.types import Message
from bot.utils import storage
import datetime

def init(app: Client) -> None:

    @app.on_message(filters.command("balance") & filters.private)
    async def balance_handler(client: Client, message: Message):
        user_id = message.from_user.id

        # ইউজারের ব্যালেন্স এবং অন্যান্য তথ্য সংগ্রহ
        user_info = storage.get_user_info(user_id)
        if not isinstance(user_info, dict):
            await message.reply(
                "❌ দুঃখিত, আপনার তথ্য পাওয়া যায়নি। অনুগ্রহ করে পরে আবার চেষ্টা করুন।"
            )
            return

        balance = user_info.get("balance", 0.0)
        success_count = user_info.get("success_count", 0)
        join_timestamp = user_info.get("join_date")

        # জয়েন তারিখ ফরম্যাটিং (যদি থাকে)
        if join_timestamp:
            try:
                join_date = datetime.datetime.fromtimestamp(join_timestamp).strftime("%d %b, %Y")
            except Exception:
                join_date = "অজানা"
        else:
            join_date = "অজানা"

        # রেসপন্স মেসেজ
        text = (
            f"🧾 আপনার অ্যাকাউন্ট তথ্য:\n\n"
            f"• 🆔 ইউজার আইডি: {user_id}\n"
            f"• ✅ সফল সেশন সংখ্যা: {success_count}\n"
            f"• 💰 ব্যালেন্স: ${balance:.2f}\n"
            f"• 📅 জয়েন করেছেন: {join_date}"
        )

        await message.reply(text)
