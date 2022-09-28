import discord
from discord.ext.commands import has_permissions 
from discord import SlashCommandGroup
from discord import slash_command
import random
import pymongo
import puzzles
from puzzles import PUZZLE_NAMEMAP


class Setup(discord.Cog):
    def __init__(self, bot: discord.Bot, database: pymongo.MongoClient):
        self.bot = bot
        self.database = database
    
    @slash_command(
        name="initialize",
        description="Setup the Escape Room framework. Command only available for administrators.",
        default_member_permissions=discord.Permissions(administrator=True)
    )

    async def initialize(self, ctx: discord.ApplicationContext):

        if self.check_validity(ctx.guild):
            await ctx.respond("Escape room already initialized in this server.", ephemeral=True)
            return

        guild = ctx.guild
        victory_role = await guild.create_role(name="Escapist")
        role = await guild.create_role(name="Escape Room Participant")
        role1 = await guild.create_role(name="Room-1")

        bot_role = discord.utils.find(lambda r: r.is_bot_managed() and 
            r in ctx.guild.get_member(self.bot.user.id).roles,
            ctx.guild.roles)

        category = await guild.create_category("Escape Room", overwrites = {
            bot_role: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            role: discord.PermissionOverwrite(view_channel=True, send_messages=False),
        })

        channel = await category.create_text_channel("Room-1", overwrites = {
            bot_role: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            role1: discord.PermissionOverwrite(view_channel=True, send_messages=True, use_application_commands = True),
        })


        self.database.insert_one({
            "guild_id": ctx.guild.id,
            "category_id": category.id,
            "victory_role": victory_role.id,
            "rooms": [
                {
                    "channel_id": channel.id,
                    "role_id": role1.id,
                    "index": 0
                }

            ],
            "puzzles": {},
            "triggers": {},
            "room_count": 1,
        })
        await ctx.respond("Running setup.", ephemeral=True)

    @slash_command(
        name="checkhealth", 
        description="Check the integrity of the escape room. Command only available for administrators.",
        default_member_permissions=discord.Permissions(administrator=True)
    )

    async def check_health(self, ctx: discord.ApplicationContext):
        await ctx.respond("Checking health.", ephemeral=True)

    @slash_command(
        name="createroom", 
        description="Add a room to the escape room. Command only available for administrators.",
        default_member_permissions=discord.Permissions(administrator=True)
    )

    async def create_room(self, ctx: discord.ApplicationContext):
        if not self.check_validity(ctx.guild):
            await ctx.respond("This server does not contain a valid escape room.")
            return

        guild_db = self.database.find_one({"guild_id": ctx.guild_id})
        bot_role = discord.utils.find(lambda r: r.is_bot_managed() and 
            r in ctx.guild.get_member(self.bot.user.id).roles,
            ctx.guild.roles)

        new_role = await ctx.guild.create_role(name=f"Room-{guild_db['room_count']+1}")
        categories = discord.utils.get(ctx.guild.categories, id=guild_db["category_id"]) 
        new_channel = await categories.create_text_channel(f"Room-{guild_db['room_count']+1}", overwrites={
            bot_role: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            new_role: discord.PermissionOverwrite(view_channel=True, send_messages=True, use_application_commands = True),
        })

        rooms = guild_data["rooms"]
        rooms.append(
            {
                "channel_id": new_channel.id,
                "role_id": new_role.id,
                "index": guild_data["room_count"]
            }
        )

        query = { "guild_id": guild_data["guild_id"] }
        self.database.update_one(query, {"$set": {"rooms": rooms} })
        self.database.update_one(query, {"$set": {"room_count": guild_data["room_count"]+1 } })


        await ctx.send_response("Creating room.", ephemeral=True)

    @slash_command(
        name="reset", 
        description="Clears an escape room and all its components. Command only available for administrators.",
        default_member_permissions=discord.Permissions(administrator=True)
    )

    async def room_purge(self, ctx: discord.ApplicationContext):
        guild_db = self.database.find_one({"guild_id": ctx.guild_id})
        if not guild_db:
            await ctx.send_response("No escape room found associated with this server.", ephemeral=True)
            return

        for room in guild_db["rooms"]:
            channel = discord.utils.get(ctx.guild.channels, id=room["channel_id"])
            await self.delete_channel(channel)
            role = discord.utils.get(ctx.guild.roles, id=room["role_id"])
            await self.delete_role(role)

        role = discord.utils.get(ctx.guild.roles, id=guild_db["role_id"])
        await self.delete_role(role)

        category = discord.utils.get(ctx.guild.categories, id=guild_db["category_id"])
        await self.delete_category(category)

        self.database.delete_one({"guild_id": ctx.guild_id})

        await ctx.send_response("Destroying room.", ephemeral=True)

    @slash_command(
        name="newpuzzle",
        description="Creates a new puzzle in an escape room puzzle room.",
        default_member_permissions=discord.Permissions(administrator=True)
    )
    async def create_puzzle(self, ctx: discord.ApplicationContext, puzzle_type: discord.Option(str), answer: discord.Option(str)):
        guild_db = self.database.find_one({"guild_id": ctx.guild_id})
        if not guild_db:
            await ctx.send_response("No escape room found associated with this server.", ephemeral=True)
            return

        c = str(random.randrange(10**5, 10**6-1))
        puzzles = guild_db["puzzles"]
        while c in puzzles:
            c = str(random.randrange(10**5, 10**6-1))

        puzzles[c] = {
            "answer": answer,
            "reward": -1,
            "next": -1
        }

        self.database.update_one({"guild_id": ctx.guild_id}, {"$set": {"puzzles": puzzles}})
        await ctx.send_response(f"Puzzle of type {puzzle_type} created with id {c}.", ephemeral=True)


    @slash_command(
        name="changeanswer", 
        description="Changes the answer for a room. Command only available for administrators.",
        default_member_permissions=discord.Permissions(administrator=True)
        options = [
            discord.Option(str, name="answer", description="New room answer", required=True)
        ]
    )
    async def change_answer(self, ctx, answer: discord.Option(str, required=True)):
        guild_query = {"guild_id": ctx.guild_id}
        guild_db = self.database.find_one(guild_query)
        if not guild_db:
            await ctx.send_response("No escape room found in this server.", ephemeral=True)
            return

        rooms = guild_db["rooms"]
        for i in range(len(rooms)):
            if rooms[i]["channel_id"] == ctx.channel_id:
                rooms[i]["answer"] = answer
                break
        else:
            await ctx.send_response("No room found in this channel.", ephemeral=True)
            return

        self.database.update_one(guild_query, {"$set": {"rooms": rooms}})
        await ctx.send_response(f"Room answer successfully updated to {answer}.", ephemeral=True)

    @slash_command(
        name="createmessage", 
        description="Causes the escape room controller to send a permanent message in a channel.",
        default_member_permissions=discord.Permissions(administrator=True)
    )

    async def new_message(self, ctx):
        await ctx.send_modal(MessageModal())

    @slash_command(
        name="trigger", 
        description="Creates a permanent, publicly visible \"trigger\" button that allows users to enter puzzle chains.",
        default_member_permissions=discord.Permissions(administrator=True)
    )
    async def create_trigger(self, ctx, label: discord.Option(str)):
        trigger = Trigger(self.database, label)
        await ctx.send_response("", view=trigger)


    def check_validity(self, guild: discord.Guild) -> bool:
        """ Checks if a guild is registered in the database. """
        guild_db = self.database.find_one({"guild_id": guild.id})
        return bool(guild_db)

    def channel_validity(self, channel: discord.TextChannel) -> bool:
        """Checks if a text channel is managed by the bot."""
        guild_db = self.database.find_one({"guild_id": guild.id})
        # assumes that guild validity has already been checked
        channels = []
        for room in guild_db["rooms"]:
            channels.append(room["channel_id"])
        return channel.id in channels

    async def delete_role(self, role: discord.Role):
        if role:
            await role.delete()

    async def delete_channel(self, channel: discord.TextChannel):
        if channel:
            await channel.delete()

    async def delete_category(self, category: discord.CategoryChannel):
        if category:
            await category.delete()
    

    @slash_command(
        name="purgeleftovers", 
        description="Command used to clean leftover roles from bot testing.",
        default_member_permissions=discord.Permissions(administrator=True)
    )
    async def leftovers(self, ctx):
        pc = 0
        for role in ctx.guild.roles:
            if role.name in ["Escapist", "Escape Room Participant"] or role.name.startswith("Room"):
                await role.delete()
                pc += 1
        await ctx.send_response(f"{pc} roles deleted.", ephemeral=True)

class MessageModal(discord.ui.Modal):

    def __init__(self):
        super().__init__(discord.ui.InputText(
            placeholder="text here...",
            max_length=1000,
            label="Body"
        ), title="Enter message content")

    async def callback(self, interaction: discord.Interaction):
        await interaction.channel.send(self.children[0].value)
        await interaction.response.send_message("Message created.", ephemeral=True)

