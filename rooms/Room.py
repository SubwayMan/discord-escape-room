import discord 
from config import DATABASE

class AnswerModalView(discord.ui.View):
    """ Base class to represent a section of an escape room."""

    def __init__(self, database):
        super().__init__(timeout=None)
        self.database = database


    @discord.ui.button(label="Answer", style=discord.ButtonStyle.green, custom_id=f"Room:Button1")
    async def submit(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild_db = self.database.find_one({"guild_id": interaction.guild_id})
        if not guild_db:
            await interaction.response.send_message("No escape room found in server. Contact server administrator.", ephemeral=True)
            return

        room = None
        rooms = guild_db["rooms"] 
        reward = guild_db["victory_role"]

        for i in range(len(rooms)):
            r = rooms[i]
            if r["channel_id"] == interaction.channel_id:
                room = r
                if i < len(rooms)-1:
                    reward = rooms[i+1]["role_id"]
                break
        else:
            await interaction.response.send_message("Invalid room. Contact server administrator.", ephemeral=True)
            return

        modal = AnswerModal(room["answer"], interaction.guild.get_role(reward))
        await interaction.response.send_modal(modal)



class AnswerModal(discord.ui.Modal):
    def __init__(self, answer:str, reward: discord.Role):
        super().__init__(
            discord.ui.InputText(
                label = "Enter Answer",
                placeholder = "answer here..."
            ),
            title = "Enter Answer"
        )
        self.reward = reward
        self.answer = answer

    async def callback(self, interaction: discord.Interaction):
        if self.children[0].value == self.answer:
            try:
                await interaction.user.add_roles(self.reward)
                await interaction.response.send_message("A door slowly opens...", ephemeral=True)
            except discord.Forbidden:
                await interaction.response.send_message("Role assignment failed. Contact server administrator.", ephemeral=True)
        else:
            await interaction.response.send_message("But nothing happened.", ephemeral=True)










            





