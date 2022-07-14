import discord


class Setup(discord.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @discord.Cog.listener(name="on_message")
    async def test(ctx, message):
        await message.pin()
        await message.channel.send("nice post dawg")
