from discord.ext import commands
import random
import asyncio
import discord

class MovingUtsu(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["mutsubyou","mutu","mutsu"])
    async def mutubyou(self, ctx, width :int=20, height : int=7, amount :int = 5, times = 5):

        drawmsgs = ["鬱病になって","自殺","してしまうよ！？"]

        cmd = ctx.message
        if cmd.reference != None:
            targetmsg = await cmd.channel.fetch_message(cmd.reference.message_id)
            targetcontent = targetmsg.content
            drawmsgs = targetcontent.split("\n")

        msg = self.drawutsus(width,height,drawmsgs,amount)
        sended : discord.Message = await ctx.send(msg[:2000])

        for i in range(times):
            await asyncio.sleep(1)
            msg = self.drawutsus(width,height,drawmsgs,amount)
            await sended.edit(content=msg[:2000])
    
    def drawutsus(self,width,height,drawmsgs,amount):

        utsu_len = len(drawmsgs)

        #outofrangeにならんよう余分にheight領域を確保
        canvas = [''.join(random.choices(["　"], k=width)) for i in range(height+utsu_len)]

        #メッセージの仕様上最初の行に文字がないとスペースが正しく反映されない為
        self.put_utsu(canvas, drawmsgs)

        for i in range(amount-1):
            self.put_utsu(canvas, drawmsgs, random.randrange(width), random.randrange(height))

        #余分な行を切り取り
        del canvas[-utsu_len:]

        msg = "\n".join(canvas)

        return msg

    def put_utsu(self, canvas, drawmsgs, insert_x=0, insert_y=0):
        canvas_length = len(canvas[0])
        for index, die in enumerate(drawmsgs):
            #描画する行を取得
            line = canvas[insert_y+index]
            #描画領域に配置済みの文字を削除
            line = line[:insert_x] + line[insert_x+len(die):]
            #描画する文字を挿入
            line = line[:insert_x] + die + line[insert_x:]
            #行の端っこをキャンバスサイズで切り取り
            line = line[:canvas_length]
            canvas[insert_y+index] = line


async def setup(bot):
    await bot.add_cog(MovingUtsu(bot))