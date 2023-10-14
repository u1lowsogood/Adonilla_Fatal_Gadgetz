from discord.ext import commands
import random
import asyncio

class InfiniteKenson(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.kensonlist = [
            ["うん","そうだね","だよね","いいと思う","だね","いいね"],
            ["んー","あー","まあ","まー"],
            ["でも","けど","だけど","やっぱり","ちょっと"],
            ["いや","いやあ","それは","うん","なんというか"],
            ["違うんじゃないかな","違うよね","違うかなあ","良くないと思う","良くないよね","だめじゃないかな",
             "駄目じゃない","ダメじゃない","だめだよね"]
        ]

    @commands.command(name="infinitekenson",aliases=["infinitykenson","インフィニティ謙遜","ik"])
    async def kenson(self, ctx):
        sends = []
        for i in range(5):
            for j in range(random.randint(1,3)):
                sampled = random.sample(self.kensonlist[i],random.randint(1,3))
                msgs = ""
                for sample in sampled:
                    msgs += sample
                    for k in range(random.randrange(4)):
                        msgs += "……"
                    if bool(random.getrandbits(1)):
                        msgs += "w"
                    if bool(random.getrandbits(1)):
                        msgs += " "
                    if random.randrange(4) == 0:
                        for k in range(random.randint(1, 3)):
                            msgs += "/n"
                sends.append(msgs)
        
        for msg in msgs:
            async with ctx.typing():
                await asyncio.sleep(random.randint(1,5))
            await ctx.channel.send(msg)


async def setup(bot):
    await bot.add_cog(InfiniteKenson(bot))