import discord
import inspect
import puzzles
import sys

async def send_puzzle(interaction: discord.Interaction, database, puzzle_id):
    """Sends a puzzle to a channel."""
    guild_db = database.find_one({"guild_id": interaction.guild_id})
    puzzle = guild_db["puzzles"][puzzle_id]
    puzzle_type = puzzle["type"]

    


class Trigger(discord.ui.View):
    """Class that provides publicly visible buttons in channels, as a means to access puzzles
    (which are ephemeral and only visible to the person who activated the trigger."""

    def __init__(self, database, label_text=""):
        super().__init__(timeout=None)
        but = discord.ui.Button(style=discord.ButtonStyle.green, label=label_text, custom_id="#")
        but.callback = self.callback
        self.add_item(but)
        self.database = database

    async def callback(self, interaction: discord.Interaction):
        guild_db = self.database.find_one({"guild_id": interaction.guild_id})
        triggers = guild_db["triggers"]
        if interaction.message.id not in triggers:
            await interaction.response.send_message("Improperly configured trigger. Contact server administrator.", ephemeral=True)
            return

        await interaction.response.send_message("Not impl", ephemeral=True)
        
# construct dict of puzzle names to classes
PUZZLE_NAMEMAP = {}
for name, obj in inspect.getmembers(puzzles):
    if inspect.isclass(obj):
        PUZZLE_NAMEMAP[name] = obj


