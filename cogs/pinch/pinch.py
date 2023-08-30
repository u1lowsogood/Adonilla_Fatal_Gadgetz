from discord.ext import commands
import random

class Pinch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["ピンチ","pinti"])
    async def pinch(self, ctx):

        sendarg = "# "

        pc_str = "ピンチチャンス"
    
        sendarg += "".join(random.choices(pc_str, k=2))+"スは\n# " if random.choice([True, False]) else random.choice(pc_str)+"ン"+random.choice(pc_str)+"は\n# "
        sendarg += "".join(random.choices(pc_str, k=3))+"!"
        
        await ctx.send(sendarg)

async def setup(bot):
    await bot.add_cog(Pinch(bot))
    

