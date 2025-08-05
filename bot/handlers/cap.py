# bot/handlers/cap.py

from pyrogram import Client, filters
from pyrogram.types import Message
from bot.utils import storage


def init(app: Client):

    @app.on_message(filters.command("cap") & filters.private)
    async def cap_list(client: Client, message: Message):
        """
        📊 দেশের রেট লিস্ট দেখায়। Admin দ্বারা সেট করা প্রতিটি দেশের মূল্য।
        """

        try:
            # যদি storage.get_country_rates() একটি async ফাংশন হয় তাহলে নিচের লাইনটি ব্যবহার করুন:
            # rates = await storage.get_country_rates()
            rates = storage.get_country_rates()

            if not rates:
                await message.reply("❌ বর্তমানে কোনো দেশের রেট সেট করা হয়নি।")
                return

            # সাজিয়ে ফরম্যাট করে রেট লিস্ট তৈরি করা
            cap_lines = [
                f"🌍 {country.upper()} ➜ ${price:.2f}"
                for country, price in sorted(rates.items())
            ]

            cap_text = "📊 উপলব্ধ দেশের ক্যাপাসিটি:\n\n" + "\n".join(cap_lines)
            await message.reply(cap_text)

        except Exception as e:
            await message.reply("⚠️ রেট লোড করতে সমস্যা হয়েছে। পরে আবার চেষ্টা করুন।")
            print(f"[cap_list] Error: {e}")
