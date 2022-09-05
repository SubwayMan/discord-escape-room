import discord 

class InteractionWrapper(discord.ui.View):
    """Class to inherit from that helps with wrapping interactable components."""
    def __init__(self, database):
        super().__init__(timeout=None)
        self.database = database

    def get_params(self, interaction):
        guild_db = self.database.find_one({"guild_id": interaction.guild_id})
        if not guild_db:
            return None

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
            return None

        return (room["answer"], interaction.guild.get_role(reward))

class AnswerModalView(InteractionWrapper):
    """ Base class to represent a section of an escape room."""

    @discord.ui.button(label="Answer", style=discord.ButtonStyle.green, custom_id=f"Room:Button1")
    async def submit(self, button: discord.ui.Button, interaction: discord.Interaction):
        params = self.get_params(interaction)
        if not params:
             await interaction.response.send_message("Configuration error. Contact server administrator.", ephemeral=True)
             return
    
        answer, role = params

        modal = AnswerModal(answer, role)
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


class GridCodeView(InteractionWrapper):
    """ Wrapper view to provide 55 grid code interactables."""

    @discord.ui.button(label="Answer", style=discord.ButtonStyle.green, custom_id=f"Button1")
    async def create_interactable(self, button: discord.ui.Button, interaction: discord.Interaction):
        params = self.get_params(interaction)
        if not params:
             await interaction.response.send_message("Configuration error. Contact server administrator.", ephemeral=True)
             return
    
        answer, role = params

        gridcode = GridCode(answer, role)
        await interaction.response.send_message(view=gridcode, ephemeral=True)


class GridCode(discord.ui.View):

    def __init__(self, answer:str, reward: discord.Role):
        super().__init__(timeout=None)
        self.data = [[0 for i in range(5)] for j in range(5)]
        for i in range(5):
            for j in range(5):
                but = discord.ui.Button(style=discord.ButtonStyle.green, label=" ", custom_id=f"{i},{j}")
                but.callback = self.callback
                self.add_item(but)

    async def callback(self, interaction:discord.Interaction, *args, **kwargs):
        r, c = map(int, interaction.custom_id.split(","))
        self.data[r][c] ^= 1
        await interaction.response.send_message(f"{r}, {c}", ephemeral=True)









            





