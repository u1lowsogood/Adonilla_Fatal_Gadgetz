from discord.ext import commands
import random

class RandomHibari(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["ランダムひばり","randommisorahibari","ランダム美空ひばり","ランダムみそらひばり"])
    async def randomhibari(self, ctx):
        sendstr = ""
        hibalyric = ["ああ","川の流れのように","穏やかに","この身任せていたい","ああ","いつまでも","ああ","ああ"]

        loopkun = random.randint(7,20)
        for a in range(loopkun):
            sendstr+=random.choice(hibalyric)
            if random.randint(0,1) == 1:
                sendstr+="\n"
        await ctx.channel.send(sendstr)

async def setup(bot):
    await bot.add_cog(RandomHibari(bot))