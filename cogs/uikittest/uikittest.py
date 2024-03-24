from discord.ext import commands
import discord

class SampleView(discord.ui.View): # UIキットを利用するためにdiscord.ui.Viewを継承する
    def __init__(self, timeout=180): # Viewにはtimeoutがあり、初期値は180(s)である
        super().__init__(timeout=timeout)
    
    @discord.ui.button(label="1つ", style=discord.ButtonStyle.success)
    async def ok(self, interaction : discord.ui.Button, button: discord.Interaction):
        await interaction.response.send_message(f"{interaction.user.mention} 残念！不正解 童貞乙……")

    @discord.ui.button(label="32つ", style=discord.ButtonStyle.success)
    async def ng(self, interaction : discord.ui.Button, button: discord.Interaction):
        await interaction.response.send_message(f"{interaction.user.mention} 正解！女性にオマンコは３２個あります。（医学的にもこれは証明されている")

class Uikittest(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def uitest(self, ctx):
        await ctx.send("Question１.\n# 女性にオマンコはいくつある？")
        view = SampleView()
        await ctx.send(view=view)

async def setup(bot):
    await bot.add_cog(Uikittest(bot))