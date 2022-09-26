import discord

class RoomBuilder(discord.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @discord.slash_command(name="createclue", description="Set up a clue message for a room. Command only available for administrators.")
    async def create_clue(self, ctx):
        await ctx.respond("Placeholder clue.")


