import discord
from discord.ext import commands
import asyncio

class WhatDoYouThinkGuys(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name="on_message")
    async def whatdoyouthinkguys(self, msg : discord.Message):

        doumou = ["みんなはどう思う？","みんなはどう思う?","みんなはどう思う"]
        has_doumou = lambda: True in [doumo in msg.content for doumo in doumou]

        if msg.author.bot == True or not has_doumou():
            return
        
        time = 20
        
        votemsg = await msg.channel.send(f"# 📢 みんなはどう思う？\n```md\n# 投票しよう！（{time}秒）```\n- そう思う👍 \n- 思わない👎",reference=msg)
        await votemsg.add_reaction("👍")
        await votemsg.add_reaction("👎")
    
        await asyncio.sleep(time)

        votemsg = await msg.channel.fetch_message(votemsg.id)
        
        resultmsg = "# 📰 結果発表\n"

        for index, reaction in enumerate(votemsg.reactions):
            think = " そう思う" if index==0 else " そう思わない" if index==1 else ""
            resultmsg += f"- {reaction.emoji}{think}： **{reaction.count}票**\n"

        await votemsg.delete()
        await msg.channel.send(resultmsg,reference=msg)

async def setup(bot):
    await bot.add_cog(WhatDoYouThinkGuys(bot))