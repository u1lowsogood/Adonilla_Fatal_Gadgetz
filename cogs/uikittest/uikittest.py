from discord.ext import commands

class Uikittest(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="satujin",aliases=["殺人","さつじん","satuzin"])
    async def satujin(self, ctx, amount : int = random.randint(0, 40)):
        sendarg = "殺人"
        for i in range(amount):
            if len(sendarg)+2 > 2000:
                break
            sendarg += "殺人"

        await ctx.send(sendarg)

async def setup(bot):
    await bot.add_cog(Uikittest(bot))