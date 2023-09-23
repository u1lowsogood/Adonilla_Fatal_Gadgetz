from discord.ext import commands
import random

class Amanda(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["アマンダ","あまんだ","amannda"])
    async def amanda(self,ctx,sex:str="セックス",amanda:str="アマンダ",hardfuck:str="ハードファック"):
        pass

async def setup(bot):
    await bot.add_cog(Amanda(bot))