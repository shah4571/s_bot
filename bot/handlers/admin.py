def init(app):
    @app.on_message(filters.command("admin") & filters.user(ADMIN_ID))
    async def admin_panel(client, message):
        await message.reply("Welcome Admin! Use /broadcast <msg> to send a broadcast.")