import discord


class Setup(discord.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @discord.slash_command(name="initialize", description="Setup the Escape Room framework. Command only available for administrators.")
    async def initialize(self, ctx: discord.ApplicationContext):
        print(type(ctx))
        guild = ctx.guild()
        await ctx.respond("Running setup.")

    @discord.slash_command(name="checkhealth", description="Check the integrity of the escape room. Command only available for administrators.")
    async def check_health(self, ctx: discord.ApplicationContext):
        await ctx.respond("Checking health.")

    @discord.slash_command(name="createroom", description="Add a room to the escape room. Command only available for administrators.")
    async def create_room(self, ctx: discord.ApplicationContext):
        await ctx.respond("Creating room.")

    @discord.slash_command(name="reset", description="Clears an escape room and all its components. Command only available for administrators.")
    async def room_purge(self, ctx: discord.ApplicationContext):
        await ctx.respond("Destroying room.")
    
