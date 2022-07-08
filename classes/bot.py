import discord


class MyBot(discord.Bot):

    def __init__(self, *args, **kwargs):
        super.__init__(args, kwargs)
        self.rooms = []
    
    @slash_command()
    async def setup(self, ctx):
        await ctx.respond("Setup to be implemented...")
