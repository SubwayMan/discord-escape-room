import discord 
import pymongo

class Room(discord.ui.View):
    """ Base class to represent a section of an escape room."""

    def __init__(self, user_id=None):
        super().__init__(timeout=None)
        self.next_room = None # channel id to redirect
        self.answer = "Placeholder"
        self.user_id = user_id

    @discord.ui.button(label="Answer", style=discord.ButtonStyle.green, custom_id=f"Room:Button1")
    async def submit(self, button: discord.ui.Button, interaction: discord.Interaction):
        modal = discord.ui.Modal(title="Submit Answer")
        modal.add_item(discord.ui.InputText(label="Answer", placeholder="type answer here..."))
        modal.callback = self.submit_answer
        await interaction.response.send_modal(modal)

    async def submit_answer(self, interaction: discord.Interaction):
        data = interaction.data["components"][0]["components"][0]["value"]

        if data == self.answer:
            await interaction.response.send_message(f"{self.user_id} Correct!", ephemeral=True)
        else:
            await interaction.response.send_message("Incorrect!", ephemeral=True)

            





