import discord
import pymongo

class Game(discord.Cog):
    """This cog is meant for organizing user/player portions of
    the escape room."""
    def __init__(self, bot: discord.Bot, mongo_client: pymongo.MongoClient):
        self.bot = bot
        self._last_member = None
        self.mongo_client = mongo_client

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
        db = self.mongo_client.EscapeRoom.production
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

        if answer == room["answer"]:
            await ctx.send_response("Correct!", ephemeral=True)
        else:
            await ctx.send_response("idk if that's right lol", ephemeral=True)



