import discord
from discord.ext import commands
import asyncio

class Selfmention(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["セルフメンション","sm"],description="/reminder [sec<30] でsec秒後に自分にメンション飛ばす\nリマインダ的な使い方はできない")
    async def selfmention(self, ctx, sec : int = 5):

        if sec > 30:
            await ctx.send("秒数は３０秒以内にしてね（リマインダというかはメンション履歴残す用なのでｗ）")
            return
        
        msg_sendedcmd = ctx.message
        msg_target = msg_sendedcmd.reference

        msg_illsend = await ctx.send(str(sec) + "秒後にメンションを送信します……",reference=msg_target)
        msg_mention = ctx.message.author.mention
    
        await asyncio.sleep(sec)

        await self.ultimatedelete(msg_illsend)
        await self.ultimatedelete(msg_sendedcmd)

        await ctx.send(msg_mention,reference=msg_target)

    async def ultimatedelete(self,msg):
        try:
            await msg.delete()
        except discord.NotFound:
            pass

async def setup(bot):
    await bot.add_cog(Selfmention(bot))