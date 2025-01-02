from discord.ext import commands

class ECO(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.economysystem = self.bot.economysystem

    @commands.command()
    async def balance(self, ctx):
        balance = self.economysystem.get_balance(str(ctx.author.id))
        await ctx.send(f"{ctx.author.mention}の残高： {balance} ADP")

async def setup(bot):
    await bot.add_cog(ECO(bot))
