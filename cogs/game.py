import discord
import pymongo



class Game(discord.Cog):
    """This cog is meant for organizing user/player portions of
    the escape room."""
    def __init__(self, bot: discord.Bot, db):
        self.bot = bot
        self._last_member = None
        self.database = db

    @discord.slash_command(
        name = "submit",
        description = "Submit your answer for this room.",
        options = [
            discord.Option(
                str, 
                name="answer",
                description="Enter your answer for this room.",
                required=True
            )
        ]
    )

    async def answer(self, ctx, answer: str):
        db = self.database
        guild_db = db.find_one({"guild_id": ctx.guild.id})
        if not guild_db:
            await ctx.respond("Not in a game room.")

        room = None
        for r in guild_db["rooms"]:
            if r["channel_id"] == ctx.channel_id:
                room = r
                break

        if not room:
            await ctx.respond("Not in a game room.")
            return

        if answer == room["answer"]:
            await ctx.send_response("A door slowly opens...", ephemeral=True)
            new_pos = room["index"] + 1
            if new_pos >= guild_db["room_count"]:
                await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, id=guild_db["victory_role"]))
            else:
                next_room = guild_db["rooms"][new_pos]
                await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, id=next_room["role_id"]))
        else:
            await ctx.send_response("Nothing happened.", ephemeral=True)
    



