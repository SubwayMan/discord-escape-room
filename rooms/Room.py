import discord 
import pymongo

class AnswerModalView(discord.ui.View):
    """ Base class to represent a section of an escape room."""

    def __init__(self, reward: discord.Role=None):
        super().__init__(timeout=None)
        self.reward = reward

    @discord.ui.button(label="Answer", style=discord.ButtonStyle.green, custom_id=f"Room:Button1")
    async def submit(self, button: discord.ui.Button, interaction: discord.Interaction):
        modal = AnswerModal(self.reward)
        await interaction.response.send_modal(modal)



class AnswerModal(discord.ui.Modal):
    def __init__(self, reward: discord.Role):
        super().__init__(
            discord.ui.InputText(
                label = "Enter Answer",
                placeholder = "answer here..."
            ),
            title = "Enter Answer"
        )
        self.reward = reward
        print(reward)
        self.answer = "nongnonog"

    async def callback(self, interaction: discord.Interaction):
        if self.children[0].value == self.answer:
            try:
                await interaction.user.add_roles(self.reward)
                await interaction.response.send_message("Correct answer.", ephemeral=True)
            except discord.Forbidden:
                await interaction.response.send_message("Role assignment failed. Contact server administrator.", ephemeral=True)
        else:
            await interaction.response.send_message("Incorrect answer.", ephemeral=True)










            





