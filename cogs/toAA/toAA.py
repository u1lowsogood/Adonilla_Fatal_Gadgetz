from discord.ext import commands
import random
from typing import Optional

class ToAA(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="2aa",aliases=["toaa","AA"])
    async def toaa(self, ctx, option : Optional[str]):
        pass


async def setup(bot):
    await bot.add_cog(ToAA(bot))