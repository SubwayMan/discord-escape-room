import os
import discord
import pymongo

from cogs import Setup, RoomBuilder
from dotenv import load_dotenv


load_dotenv(".env")

mongo_client = pymongo.MongoClient(os.getenv("MONGO_URL"))

bot = discord.Bot()
bot.add_cog(Setup(bot, mongo_client))
bot.add_cog(RoomBuilder(bot))
bot.run(os.getenv("TOKEN"))

