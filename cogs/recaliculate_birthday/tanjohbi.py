import discord
from discord.ext import commands
import asyncio
from textwrap import dedent
import datetime

class Tanjohbi(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self,msg : discord.Message):

        if msg.author == self.bot.user:
            return
        
        if not ("誕生日" in msg.content or "たんじょうび" in msg.content):
            return
        
        current_time = datetime.datetime.now()

        day_chakushou = current_time - datetime.timedelta(days=266)
        day_jusei = day_chakushou - datetime.timedelta(days=9,hours=10,minutes=24)
        day_sex = day_jusei - datetime.timedelta(days=3,hours=6,minutes=4)

        sendmsg = dedent(f"""
        {msg.author.mention}

        誕生日おめでとうございます！
        # 計算すると、あなたのお母様は **__{day_sex.strftime('%m月%d日')}__** に **__セックス__** をしましたね笑

        ```md
        # 【あなたのお母様の詳細なセックス情報】
        ・セックス日時： {day_sex.strftime('%m月%d日 %H時%M分')} (299日前)
        ・着床日時： {day_chakushou.strftime('%m月%d日 %H時%M分')} ({299+9}日前)
        ・受精日時： {day_jusei.strftime('%m月%d日 %H時%M分')} ({299+9+3}日前)
        ```
        """
        )
    
        await msg.channel.send(sendmsg)

async def setup(bot):
    await bot.add_cog(Tanjohbi(bot))