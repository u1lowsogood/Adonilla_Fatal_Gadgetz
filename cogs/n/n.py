from discord.ext import commands
import pykakasi
import random
import re

class N(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.big_n = "\n　＿　\n　　＿／\n\n"
        self.ns = ["ン","ﾝ","ん","n"]

    @commands.command(aliases=["ン"])
    async def n(self, ctx):
        cmd = ctx.message
        if cmd.reference == None:
            await cmd.channel.send("このコマンドは返信内で使用してね（右クリック → 返信）")
            return
        
        targetmsg = await cmd.channel.fetch_message(cmd.reference.message_id)
        targetcontent = targetmsg.content

        kks = pykakasi.kakasi()
        re_kanji = re.compile(r'^[\u4E00-\u9FD0]+$')
        msg = ""

        """for converted in kks.convert(targetcontent):
            print(converted['orig'] + converted['hira'])
            if "ん" in converted['hira']:
                moji = converted['orig'] + self.big_n
            else:
                moji = converted['orig']
            msg += moji"""
        
        for moji in targetcontent:
            if re_kanji.fullmatch(moji):
                converted = kks.convert(moji)
                if "ん" in converted[0]['hira']:
                    moji = moji + self.big_n
            else:
                for m in self.ns:
                    moji = moji.replace(m,self.big_n)
            msg += moji

        await ctx.send(msg)

async def setup(bot):
    await bot.add_cog(N(bot))