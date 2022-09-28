import os
import discord
import pymongo

from setup import *
from puzzles import *
from helpers import Trigger
from dotenv import load_dotenv

load_dotenv("../../.env")
TOKEN = os.getenv("TOKEN")
CLIENT = pymongo.MongoClient(os.getenv("MONGO_URL"))
DATABASE = CLIENT.EscapeRoom.production

ints = discord.Intents.default()
ints.message_content = True

bot = discord.Bot(intents=ints)

@bot.listen()
async def on_ready():
    bot.add_view(Trigger(DATABASE))

bot.add_cog(Setup(bot, DATABASE))




bot.run(TOKEN)

