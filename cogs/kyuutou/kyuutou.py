from discord.ext import commands
import random

class Kyuutou(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["給湯","kyuto","kyutou"])
    async def kyuutou(self, ctx):

        if random.randint(0,5) == 1:
            await ctx.channel.send("給湯 温度を " + str(random.randint(10000,9999999)) + "度に 設定します")
        else:
            await ctx.channel.send("給湯 温度を " + str(random.randint(0,70)) + "度に 設定します")

async def setup(bot):
    await bot.add_cog(Kyuutou(bot))