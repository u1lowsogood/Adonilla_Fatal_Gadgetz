from discord.ext import commands
import random

class IncUterus(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["sikyu","しきゅう","子宮"])
    async def sikyuu(self, ctx):
        sendarg = "# 子宮が " + str(random.randint(-99999999,999999999)) + "個 ある"
        await ctx.send(sendarg)

async def setup(bot):
    await bot.add_cog(IncUterus(bot))