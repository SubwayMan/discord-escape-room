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
        victory_role = await guild.create_role(name="Escapist")
        role = await guild.create_role(name="Escape Room Participant")
        perms = discord.PermissionOverwrite()
        category = await guild.create_category("Escape Room", overwrites={role: perms})
        channel = await category.create_text_channel("Room-1")


        self.mongo_client.EscapeRoom.production.insert_one({
            "guild_id": ctx.guild.id,
            "category_id": category.id,
            "role_id": victory_role.id,
            "rooms": [
                {
                    "channel_id": channel.id,
                    "role_id": role.id,
                    "answer": "Bongobong",
                    "index": 0
                }

            ],
            "room_count": 1,
        })
        await ctx.respond("Running setup.")

    @discord.slash_command(name="checkhealth", description="Check the integrity of the escape room. Command only available for administrators.")
    async def check_health(self, ctx: discord.ApplicationContext):
        await ctx.respond("Checking health.")

    @discord.slash_command(name="createroom", description="Add a room to the escape room. Command only available for administrators.")
    async def create_room(self, ctx: discord.ApplicationContext):
        if not self.check_validity(ctx.guild):
            await ctx.respond("This server does not contain a valid escape room.")
            return

        await ctx.respond("Creating room.")

    @discord.slash_command(name="reset", description="Clears an escape room and all its components. Command only available for administrators.")
    async def room_purge(self, ctx: discord.ApplicationContext):
        value = self.mongo_client.EscapeRoom.production.find_one({"guild_id": ctx.guild_id})
        if value:
            role = discord.utils.get(ctx.guild.roles, id=value["role_id"])
            await role.delete()
            for room in value["rooms"]:
                role = discord.utils.get(ctx.guild.roles, id=room["role_id"])
                await role.delete()
                channel = discord.utils.get(ctx.guild.channels, id=room["channel_id"])
                await channel.delete()
            category = discord.utils.get(ctx.guild.categories, id=value["category_id"])
            await category.delete()

        self.mongo_client.EscapeRoom.production.delete_one({"guild_id": ctx.guild_id})

        await ctx.respond("Destroying room.")

    def check_validity(self, guild: discord.Guild):
        """ Checks if a guild is registered in the database. """
        guild_db = self.mongo_client.EscapeRoom.production.find_one({"guild_id": guild.id})
        return bool(guild_db)



