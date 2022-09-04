import os
import discord
import pymongo


from cogs import Setup, RoomBuilder, Game
from rooms import Room
from dotenv import load_dotenv

class PersistentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Green", style=discord.ButtonStyle.green, custom_id="persistent_view:green")
    async def green(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("This is green.", ephemeral=True)

    @discord.ui.button(label="Red", style=discord.ButtonStyle.red, custom_id="persistent_view:red")
    async def red(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("This is red.", ephemeral=True)

    @discord.ui.button(label="Grey", style=discord.ButtonStyle.grey, custom_id="persistent_view:grey")
    async def grey(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("This is grey.", ephemeral=True)

load_dotenv(".env")


mongo_client = pymongo.MongoClient(os.getenv("MONGO_URL"))

ints = discord.Intents.default()
ints.message_content = True

bot = discord.Bot(intents=ints)

@bot.listen()
async def on_ready():
    bot.add_view(PersistentView())
    bot.add_view(Room())

bot.add_cog(Setup(bot, mongo_client))
bot.add_cog(Game(bot, mongo_client))
bot.add_cog(RoomBuilder(bot))

@bot.command()
async def prepare(ctx):
    await ctx.respond("test", view=PersistentView(), ephemeral=True)

@bot.command()
async def modaltest(ctx):
    await ctx.respond("test", view=Room(ctx.user.id), ephemeral=True)

bot.run(os.getenv("TOKEN"))

