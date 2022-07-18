import discord
import pymongo


class Setup(discord.Cog):
    def __init__(self, bot, mongo_client: pymongo.MongoClient):
        self.bot = bot
        self._last_member = None
        self.mongo_client = mongo_client

    @discord.slash_command(name="initialize", description="Setup the Escape Room framework. Command only available for administrators.")
    async def initialize(self, ctx: discord.ApplicationContext):
        guild = ctx.guild
        role = await guild.create_role(name="Escapist")
        perms = discord.PermissionOverwrite()
        category = await guild.create_category("Escape Room", overwrites={role: perms})

        self.mongo_client.EscapeRoom.production.insert_one({
            "guild_id": ctx.guild.id,
            "category_id": category.id,
            "role_id": role.id,
            "rooms": [],
            "room_count": 0,
        })
        await ctx.respond("Running setup.")

    @discord.slash_command(name="checkhealth", description="Check the integrity of the escape room. Command only available for administrators.")
    async def check_health(self, ctx: discord.ApplicationContext):
        await ctx.respond("Checking health.")

    @discord.slash_command(name="createroom", description="Add a room to the escape room. Command only available for administrators.")
    async def create_room(self, ctx: discord.ApplicationContext):
        await ctx.respond("Creating room.")

    @discord.slash_command(name="reset", description="Clears an escape room and all its components. Command only available for administrators.")
    async def room_purge(self, ctx: discord.ApplicationContext):
        value = self.mongo_client.EscapeRoom.production.find_one({"guild_id": ctx.guild_id})
        if value:
            category = discord.utils.get(ctx.guild.categories, id=value["category_id"])
            await category.delete()
            role = discord.utils.get(ctx.guild.roles, id=value["role_id"])
            await role.delete()

        self.mongo_client.EscapeRoom.production.delete_one({"guild_id": ctx.guild_id})

        await ctx.respond("Destroying room.")
    
