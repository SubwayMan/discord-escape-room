import discord 

class Trigger(discord.ui.View):
    """Class that provides publicly visible buttons in channels, as a means to access puzzles
    (which are ephemeral and only visible to the person who activated the trigger."""

    def __init__(self, database, label_text=""):
        super().__init__(timeout=None)
        but = discord.ui.Button(style=discord.ButtonStyle.green, label=label_text, custom_id="#", callback=self.callback)
        self.add_item(but)
        self.database = database

    async def callback(self, interaction: discord.Interaction):
        guild_db = self.database.find_one({"guild_id": interaction.guild_id})
        triggers = guild_db["triggers"]
        if interaction.message.id not in triggers:
            await interaction.response.send_message("Improperly configured trigger. Contact server administrator.", ephemeral=True)
            return

        await interaction.response.send_message("Not impl", ephemeral=True)
        print(triggers[message_id])
        




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
    """ Wrapper view to provide 5x5 grid code interactables."""

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
        self.buttons = [[None for i in range(5)] for j in range(5)]
        self.answer = answer
        self.reward = reward

        for i in range(5):
            for j in range(5):
                self.buttons[i][j] = discord.ui.Button(style=discord.ButtonStyle.green, label=" ", custom_id=f"{i},{j}")
                self.buttons[i][j].callback = self.callback
                self.add_item(self.buttons[i][j])

    async def callback(self, interaction:discord.Interaction):
        r, c = map(int, interaction.custom_id.split(","))
        self.data[r][c] ^= 1
        if self.data[r][c] == 1:
            self.buttons[r][c].style = discord.ButtonStyle.red
        else:
            self.buttons[r][c].style = discord.ButtonStyle.green

        current_state = "".join(("".join(map(str, row)) for row in self.data))
        if current_state == self.answer:
            for row in self.buttons:
                for button in row:
                    button.disabled = True

        await interaction.response.edit_message(view=self)
        if current_state == self.answer:
            try:
                await interaction.user.add_roles(self.reward)
                await interaction.followup.send("A door slowly opens...", ephemeral=True)
            except discord.Forbidden:
                await interaction.followup.send("Role assignment failed. Contact server administrator.", ephemeral=True)


class PinCodeView(InteractionWrapper):
    """ Wrapper view to provide 5x5 grid code interactables."""

    @discord.ui.button(label="Answer", style=discord.ButtonStyle.green, custom_id=f"Button1")
    async def create_interactable(self, button: discord.ui.Button, interaction: discord.Interaction):
        params = self.get_params(interaction)
        if not params:
             await interaction.response.send_message("Configuration error. Contact server administrator.", ephemeral=True)
             return
    
        answer, role = params
        if not answer[0].isdigit():
            await interaction.response.send_message("Room answer is improperly configured. Contact server administrator.", ephemeral=True)
            return

        gridcode = PinCode(answer, role)
        await interaction.response.send_message(" ".join("-" * len(answer)), view=gridcode, ephemeral=True)


class PinCode(discord.ui.View):

    def __init__(self, answer:str, reward: discord.Role):
        super().__init__(timeout=None)
        self.answer = answer
        self.reward = reward
        self.value = ""
        self.buttons = []
        for i in range(1, 10):
            self.buttons.append(discord.ui.Button(style=discord.ButtonStyle.green, label=str(i), custom_id=str(i), row=(i-1)//3))
            self.buttons[-1].callback = self.callback
            self.add_item(self.buttons[-1])

    async def callback(self, interaction:discord.Interaction):
        id = interaction.custom_id
        self.value += id
        await interaction.response.edit_message(content=" ".join(self.value + "-" * (len(self.answer) - len(self.value))), view=self)
        if len(self.value) == len(self.answer):
            if self.value == self.answer:
                for but in self.buttons:
                    but.disabled = True

                await interaction.edit_original_message(content=" ".join(self.value), view=self)

                try:
                    await interaction.user.add_roles(self.reward)
                    await interaction.followup.send("A door slowly opens...", ephemeral=True)
                except discord.Forbidden:
                    await interaction.followup.send("Role assignment failed. Contact server administrator.", ephemeral=True)
            else:
                await interaction.edit_original_message(content=" ".join("-" * len(self.answer)), view=self)
                self.value = ""



# A dict that maps an id identifying a puzzle with its class
PUZZLE_IDS = {
    "1": InteractionWrapper
}

        





    

    
        

        









            





