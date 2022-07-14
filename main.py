import os
import discord
from cogs import Setup, RoomBuilder
from dotenv import load_dotenv


load_dotenv(".env")

bot = discord.Bot()
bot.add_cog(Setup(bot))
bot.add_cog(RoomBuilder(bot))
bot.run(os.getenv("TOKEN"))

#@bot.command(description="Initialize the escape room. Dangerous command only available to admins.")
#async def initialize(ctx):
