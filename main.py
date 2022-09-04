import os
import discord
import pymongo
import config


from cogs import Setup, RoomBuilder, Game
from rooms import *
from dotenv import load_dotenv

load_dotenv(".env")



ints = discord.Intents.default()
ints.message_content = True

bot = discord.Bot(intents=ints)

@bot.listen()
async def on_ready():
    bot.add_view(AnswerModalView(config.DATABASE))

bot.add_cog(Setup(bot, config.DATABASE))
bot.add_cog(Game(bot, config.DATABASE))
bot.add_cog(RoomBuilder(bot))

@bot.command()
async def modaltest(ctx):
    await ctx.channel.send(view=AnswerModalView(config.DATABASE))
    await ctx.respond("View successfully created", ephemeral=True)

bot.run(config.TOKEN)

