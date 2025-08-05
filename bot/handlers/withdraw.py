from pyrogram import Client, filters
from pyrogram.types import Message

def init(app: Client):
    @app.on_message(filters.command("withdraw") & filters.private)
    async def withdraw_command(client: Client, message: Message):
        """
        💸 Withdraw কমান্ড হ্যান্ডলার।
        বর্তমানে ফিচারটি সক্রিয় নয়, ভবিষ্যতে যুক্ত হবে।
        """
        await message.reply("💸 Withdraw ফিচারটি খুব শীঘ্রই আসছে! অনুগ্রহ করে অপেক্ষা করুন।")
