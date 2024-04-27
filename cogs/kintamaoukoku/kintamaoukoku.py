from discord.ext import commands
import random
import asyncio
import discord

class KintamaOukoku(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["金玉王国","金玉王国回転","kos"])
    async def kintamaoukokuspinning(self, ctx, content : str = "金玉王国", amount : int = 10):

        if len(content) < 4:
            content = content.ljust(4)
        else:
            content = content[:4]

        sended : discord.Message = await ctx.send(f"# {content[0]}　{content[1]}\n　   ↖️\n# {content[2]}　{content[3]}")

        for i in range(amount):
            await asyncio.sleep(1)
            msg = self.spinner(content,i)
            await sended.edit(content=msg)

    def spinner(self, content, period):
        junbans = [[0,1,2,3],[2,0,3,1],[3,2,1,0],[1,3,0,2]]
        junban = junbans[(period+1)%4]
        shaft = self.getshaft(period)
        return f"# {content[junban[0]]}　{content[junban[1]]}\n　   {shaft}\n# {content[junban[2]]}　{content[junban[3]]}"
    
    def getshaft(self, period):
        if period%4==0:
            return "↗️"
        elif period%4==1:
            return "↘️"
        elif period%4==2:
            return "↙️"
        elif period%4==3:
            return "↖️"

async def setup(bot):
    await bot.add_cog(KintamaOukoku(bot))