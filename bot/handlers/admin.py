# bot/handlers/admin.py

from pyrogram import Client, filters
from pyrogram.types import Message
from bot.config import ADMIN_ID
from bot import storage  # Ensure you have this module for user management
import asyncio
from pyrogram.errors import FloodWait, UserIsBlocked, PeerIdInvalid


def init(app: Client):

    @app.on_message(filters.command("admin") & filters.user(ADMIN_ID) & filters.private)
    async def admin_panel(client: Client, message: Message):
        """
        অ্যাডমিন প্যানেল কমান্ড।
        শুধুমাত্র ADMIN_ID এর জন্য কাজ করবে এবং প্রাইভেট চ্যাটে।
        """
        text = (
            "🛡️ স্বাগতম, অ্যাডমিন!\n\n"
            "ব্যবহারযোগ্য কমান্ড:\n"
            "/broadcast <মেসেজ> - সকল ব্যবহারকারীর কাছে বার্তা পাঠাও।\n"
            "/stats - বটের স্ট্যাটিস্টিকস দেখাও।\n"
        )
        await message.reply(text)

    @app.on_message(filters.command("broadcast") & filters.user(ADMIN_ID) & filters.private)
    async def broadcast_message(client: Client, message: Message):
        """
        সকল ব্যবহারকারীর কাছে ব্রডকাস্ট মেসেজ পাঠানো।
        কমান্ড: /broadcast <মেসেজ>
        """
        if len(message.command) < 2:
            await message.reply("❌ মেসেজটি লিখো। উদাহরণ: /broadcast Hello everyone!")
            return

        broadcast_text = message.text.split(None, 1)[1]

        user_ids = await storage.get_all_user_ids()

        success_count = 0
        failed_count = 0

        for user_id in user_ids:
            try:
                await client.send_message(user_id, broadcast_text)
                success_count += 1
                await asyncio.sleep(0.1)  # Avoid hitting flood limits
            except FloodWait as e:
                await asyncio.sleep(e.value)
                try:
                    await client.send_message(user_id, broadcast_text)
                    success_count += 1
                except Exception:
                    failed_count += 1
            except (UserIsBlocked, PeerIdInvalid):
                failed_count += 1
            except Exception as e:
                print(f"❌ Error sending to {user_id}: {e}")
                failed_count += 1

        await message.reply(
            f"✅ ব্রডকাস্ট সম্পন্ন!\n\nসফল: {success_count}\nব্যর্থ: {failed_count}"
        )
