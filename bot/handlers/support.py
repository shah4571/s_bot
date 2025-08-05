def init(app):
    @app.on_message(filters.command("support"))
    async def support(client, message):
        await message.reply("🛠 Contact @SupportBot for help.")