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
    bot.add_view(GridCodeView(config.DATABASE))

bot.add_cog(Setup(bot, config.DATABASE))
bot.add_cog(Game(bot, config.DATABASE))
bot.add_cog(RoomBuilder(bot))

@bot.command()
async def modaltest(ctx):
    await ctx.channel.send(view=AnswerModalView(config.DATABASE))
    await ctx.respond("View successfully created", ephemeral=True)

@bot.command()
async def gridtest(ctx):
    await ctx.channel.send(view=GridCodeView(config.DATABASE))
    await ctx.respond("View successfully created", ephemeral=True)

@bot.command()
async def joingame(ctx):
    guild_db = config.DATABASE.find_one({"guild_id": ctx.guild_id})
    if not guild_db:
        ctx.send_response("No escape room set up in this server.", ephemeral=True)
        return
    role = ctx.guild.get_role(guild_db["rooms"][0]["role_id"])
    await ctx.user.add_roles(role)
    

    


bot.run(config.TOKEN)

