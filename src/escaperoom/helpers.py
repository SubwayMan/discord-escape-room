import discord
import inspect
import sys

async def send_puzzle(interaction: discord.Interaction, database, puzzle_id):
    """Sends a puzzle to a channel."""
    guild_db = database.find_one({"guild_id": interaction.guild_id})
    puzzle = guild_db["puzzles"][puzzle_id]
    if puzzle["type"] not in PUZZLE_NAMEMAP:
        await interaction.followup.send("Improperly configured puzzle. Contact server administrator.", ephemeral=True)

    puzzle_type = PUZZLE_NAMEMAP[puzzle["type"]]
    puzzle_next = puzzle["next"] # next view, or -1 if None
    puzzle_reward = puzzle["reward"] # discord role id, or -1 if none
    puzzle_answer = puzzle["answer"]

    attach = puzzle_type(puzzle_answer, puzzle_reward, puzzle_next)
    if isinstance(attach, discord.ui.Modal):
        await interaction.response.send_modal(attach)
    else:
        await interaction.followup.send("", view=attach, ephemeral=True)


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

        trigger = triggers[interaction.message.id]
        if trigger["view_id"] not in guild_db["puzzles"]:
            await interaction.response.send_message("No puzzle found to trigger.", ephemeral=True)
            return

        await send_puzzle(interaction, self.database, trigger["view_id"])


class Puzzle():
    def __init__(self, database, answer:str, reward, next):
        self.database = database
        self.answer = answer
        self.reward = reward
        self.next = next

    async def progress(self, interaction: discord.Interaction):
        if self.reward != -1:
            role = interaction.guild.get_role(self.reward)
            try:
                await interaction.user.add_roles(role)
                await interaction.followup.send("A door slowly opens...", ephemeral=True)
            except discord.Forbidden:
                await interaction.followup.send("Role assignment failed. Contact server administrator.", ephemeral=True)

        if self.next != -1:
            puzzles = self.database.find_one({"guild_id": interaction.guild_id})["puzzles"]
            if self.next in puzzles:
                await send_puzzle(interaction, self.database, self.next)
            else:
                await interaction.followup.send(f"Missing puzzle with id {self.next}. Contact server administrator.", ephemeral=True)

# Store dict of puzzle names to classes
# This is modified after import (to resolve circular dependencies)
PUZZLE_NAMEMAP = {}

def test():
    print(PUZZLE_NAMEMAP)

