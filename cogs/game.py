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
        await ctx.respond("idk if that's right lol")



