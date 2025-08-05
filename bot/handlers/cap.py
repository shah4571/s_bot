def init(app):
    @app.on_message(filters.command("cap"))
    async def cap_list(client, message):
        rates = storage.get_country_rates()
        cap_text = "\n".join([f"{k}: ${v}" for k, v in rates.items()])
        await message.reply(f"📊 Country Rates:\n{cap_text}")