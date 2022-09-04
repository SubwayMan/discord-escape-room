import discord
import pymongo



class Game(discord.Cog):
    """This cog is meant for organizing user/player portions of
    the escape room."""
    def __init__(self, bot: discord.Bot, db):
        self.bot = bot
        self._last_member = None
        self.database = db

