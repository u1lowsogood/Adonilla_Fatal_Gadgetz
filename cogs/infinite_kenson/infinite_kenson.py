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
             "駄目じゃない？","ダメじゃない？","だめだよね","ダメだよ","良くないよ","駄目","やめたほうが良いよね","やめろ"]
        ]

    @commands.command(name="infinitekenson",aliases=["infinitykenson","インフィニティ謙遜","ik"])
    async def kenson(self, ctx):
        target = ctx.message.author
        if ctx.message.reference != None and ctx.message.reference.resolved != None:
            target = ctx.message.reference.resolved.author

        sends = []
        for i in range(5):
            for j in range(random.randint(1,3)):
                sampled = random.sample(self.kensonlist[i],random.randint(1,3))
                msgs = ""
                for sample in sampled:
                    msgs += sample
                    if random.randrange(10) == 0:   
                        msgs += target.nick + random.choice(["さんはそう思うんだよね","さん、",
                                                             "さんの意見だけど","は？","って名前ダサいよね","さんは本当にそう思ってる？",
                                                             "さんに同意はするけど","さんはどうなの？"])
                    if random.randrange(20) == 0:   
                        msgs += target.mention
                    if random.randrange(4) == 0 and i != 4:
                        msgs += "？"
                    for k in range(random.randrange(4)):
                        msgs += "……"
                    if random.randrange(4) == 0:
                        msgs += "笑"
                    if random.randrange(3) == 0:
                        msgs += "w "
                    if bool(random.getrandbits(1)):
                        msgs += " "

                    if random.randrange(4) == 0:
                        for k in range(random.randint(1, 3)):
                            msgs += "\n"
                
                sends.append(msgs)

                if random.randrange(7) == 0:
                        sends.append(target.mention + random.choice(
                            [""," 聞いてる？"," 話してるんだけど"," ねえ"," あの～"," 真面目に聞いてる？"," ちゃんと聞いてる？"," 見てる？","お～い笑"]))
        
        for send in sends:
            await asyncio.sleep(random.randint(0,2))
            async with ctx.typing():
                await asyncio.sleep(random.randint(1,4))
            await ctx.channel.send(send)


async def setup(bot):
    await bot.add_cog(InfiniteKenson(bot))