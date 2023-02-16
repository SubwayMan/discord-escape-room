import discord 
import sys, inspect
from helpers import Puzzle, PUZZLE_NAMEMAP, test
            

class AnswerModal(Puzzle, discord.ui.Modal):
    def __init__(self, database, answer:str, reward: discord.Role, next: int):
        Puzzle.__init__(self, database, answer, reward, next)
        discord.ui.Modal.__init__(self, 
            discord.ui.InputText(
                label = "Enter Answer",
                placeholder = "answer here..."
            ),
            title = "Enter Answer"
        )

    async def callback(self, interaction: discord.Interaction):
        interaction.response.defer()
        if self.children[0].value == self.answer:
            await self.progress(interaction)
        else:
            await interaction.followup.send("But nothing happened.", ephemeral=True)


class GridCode(Puzzle, discord.ui.View):

    def __init__(self, database, answer:str, reward: discord.Role, next: int):
        Puzzle.__init__(self, database, answer, reward, next)
        discord.ui.View.__init__(self, timeout=None)
        self.data = [[0 for i in range(5)] for j in range(5)]
        self.buttons = [[None for i in range(5)] for j in range(5)]

        for i in range(5):
            for j in range(5):
                self.buttons[i][j] = discord.ui.Button(style=discord.ButtonStyle.green, label="O", custom_id=f"{i},{j}")
                self.buttons[i][j].callback = self.callback
                self.add_item(self.buttons[i][j])

    def __str__(self):
        return ""

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
            await self.progress(interaction)



class PinCode(Puzzle, discord.ui.View):

    def __init__(self, database, answer:str, reward: discord.Role, next: int):
        Puzzle.__init__(self, database, answer, reward, next)
        discord.ui.View.__init__(self, timeout=None)
        self.value = ""
        self.buttons = []
        for i2 in range(1, 11):
            i = i2%10
            self.buttons.append(discord.ui.Button(style=discord.ButtonStyle.green, label=str(i), custom_id=str(i), row=max(0, (i-1)//3)))
            self.buttons[-1].callback = self.callback
            self.add_item(self.buttons[-1])

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        id = interaction.custom_id
        self.value += id
        await interaction.edit_original_message(content=" ".join(self.value + "-" * (len(self.answer) - len(self.value))), view=self)
        if len(self.value) == len(self.answer):
            if self.value == self.answer:
                for but in self.buttons:
                    but.disabled = True

                await interaction.edit_original_message(content=" ".join(self.value), view=self)
                await self.progress(interaction)

            else:
                await interaction.edit_original_message(content=" ".join("-" * len(self.answer)), view=self)
                self.value = ""


class FourButtonCode(Puzzle, discord.ui.View):
    def __init__(self, database, answer:str, reward: discord.Role, next: int):
        Puzzle.__init__(self, database, answer, reward, next)
        discord.ui.View.__init__(self, timeout=None)

        self.display = ["-" for i in range(len(answer)-1)]
        self.value = ""
        self.buttons = []

        for i in range(4):
            self.buttons.append(discord.ui.Button(label=" ", style=discord.ButtonStyle.gray, custom_id=str(i), row=i//2))
            self.add_item(self.buttons[-1])
            self.buttons[-1].callback = self.callback

        if answer[0] == "#":
            self.buttons[0].emoji = "🔵"
            self.buttons[1].emoji = "🔴"
            self.buttons[2].emoji = "🟡"
            self.buttons[3].emoji = "🟢"

        elif answer[0] == "&":
            self.buttons[0].emoji = "⬅️"
            self.buttons[1].emoji = "⬇️"
            self.buttons[2].emoji = "➡️"
            self.buttons[3].emoji = "⬆️"

        elif answer[0] == "%":
            self.buttons[0].emoji = "↙️"
            self.buttons[1].emoji = "↘️"
            self.buttons[2].emoji = "↖️"
            self.buttons[3].emoji = "↗️"

        elif answer[0] == "$":
            self.buttons[0].emoji = "1️⃣"
            self.buttons[1].emoji = "2️⃣"
            self.buttons[2].emoji = "3️⃣"
            self.buttons[3].emoji = "4️⃣"

        self.answer = answer[1:]

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        id = interaction.custom_id
        self.value += id
        if self.buttons[0].emoji:
            self.display[len(self.value)-1] = str(self.buttons[int(id)].emoji)
        else:
            self.display[len(self.value)-1] = "*"

        await interaction.edit_original_message(content=" ".join(self.display), view=self)
        if len(self.value) == len(self.answer):
            if self.value == self.answer:
                for but in self.buttons:
                    but.disabled = True

                await interaction.edit_original_message(content=" ".join(self.display), view=self)
                await self.progress(interaction)

            else:
                await interaction.edit_original_message(content=" ".join("-" * len(self.answer)), view=self)
                self.value = ""
                self.display = ["-" for i in range(len(self.answer))]

for name, obj in inspect.getmembers(sys.modules[__name__]):
    if inspect.isclass(obj) and obj != Puzzle:
        PUZZLE_NAMEMAP[name] = obj

if __name__ == "__main__":
    test()

        

