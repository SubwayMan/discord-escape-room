import discord
import pymongo


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


class Game(discord.Cog):
    """This cog is meant for organizing user/player portions of
    the escape room."""
    def __init__(self, bot: discord.Bot, mongo_client: pymongo.MongoClient):
        self.bot = bot
        self._last_member = None
        self.mongo_client = mongo_client

    @discord.slash_command(
        name = "submit",
        description = "Submit your answer for this room.",
        options = [
            discord.Option(
                str, 
                name="answer",
                description="Enter your answer for this room.",
                required=True
            )
        ]
    )

    async def answer(self, ctx, answer: str):
        db = self.mongo_client.EscapeRoom.production
        guild_db = db.find_one({"guild_id": ctx.guild.id})
        if not guild_db:
            await ctx.respond("Not in a game room.")

        room = None
        for r in guild_db["rooms"]:
            if r["channel_id"] == ctx.channel_id:
                room = r
                break

        if not room:
            await ctx.respond("Not in a game room.")
            return

        if answer == room["answer"]:
            await ctx.send_response("A door slowly opens...", ephemeral=True)
            new_pos = room["index"] + 1
            if new_pos >= guild_db["room_count"]:
                await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, id=guild_db["victory_role"]))
            else:
                next_room = guild_db["rooms"][new_pos]
                await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, id=next_room["role_id"]))
        else:
            await ctx.send_response("Nothing happened.", ephemeral=True)
    
    @discord.slash_command(name="butt")
    async def butt(self, ctx):
        view = PersistentView()
        await ctx.send_response("b", view=view)



