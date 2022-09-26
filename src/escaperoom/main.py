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
    bot.add_view(AnswerModalView(DATABASE))
    bot.add_view(GridCodeView(DATABASE))
    bot.add_view(PinCodeView(DATABASE))

bot.add_cog(Setup(bot, DATABASE))

@bot.command()
async def modaltest(ctx):
    await ctx.channel.send(view=AnswerModalView(DATABASE))
    await ctx.respond("View successfully created", ephemeral=True)

@bot.command()
async def gridtest(ctx):
    await ctx.channel.send(view=GridCodeView(DATABASE))
    await ctx.respond("View successfully created", ephemeral=True)

@bot.command()
async def pintest(ctx):
    await ctx.channel.send(view=PinCodeView(DATABASE))
    await ctx.respond("View successfully created", ephemeral=True)

@bot.command()
async def joingame(ctx):
    guild_db = DATABASE.find_one({"guild_id": ctx.guild_id})
    if not guild_db:
        ctx.send_response("No escape room set up in this server.", ephemeral=True)
        return
    role = ctx.guild.get_role(guild_db["rooms"][0]["role_id"])
    await ctx.user.add_roles(role)
    

    


bot.run(TOKEN)

