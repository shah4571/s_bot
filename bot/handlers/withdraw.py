def init(app):
    @app.on_message(filters.command("withdraw"))
    async def withdraw(client, message):
        await message.reply("💸 Withdraw feature coming soon!")