def init(app):
    @app.on_message(filters.command("balance"))
    async def balance(client, message):
        user_id = message.from_user.id
        bal = storage.get_balance(user_id)
        await message.reply(f"💰 Your balance: ${bal:.2f}")