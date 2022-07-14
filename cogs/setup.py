import discord


class Setup(discord.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @discord.slash_command(name="initialize", description="Setup the Escape Room framework. Command only available for administrators.")
    async def initialize(self, ctx):
        await ctx.respond("Running setup.")

    @discord.slash_command(name="checkhealth", description="Verify the functionality of all the escape room components. Command only available for administrators.")
    async def check_health(self, ctx):
        await ctx.respond("Checking health.")

    @discord.slash_command(name="createroom", description="Add a room to the escape room. Command only available for administrators.")
    async def create_room(self, ctx):
        await ctx.respond("Creating room.")
    
