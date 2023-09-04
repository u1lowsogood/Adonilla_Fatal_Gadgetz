from discord.ext import commands
import numpy as np
import cv2
import io
import requests
import discord

class Gabigabi(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["gabi","ガビガビ"])
    async def gabigabi(self, ctx, quality : int = 2):
        if ctx.message.reference == None:
            await ctx.send("このコマンドは返信\n # と一緒に\n # 利用してみてねｗ←ｗ")
            return
        
        elif quality < 0:
            await ctx.send("負の回数は無理ｗ")
            return
        
        feched_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if feched_message.attachments == []:
            await ctx.send("返\n信\n# 先のメ\nッセージは画像である必要が……\n # ある")
            return
        
        resp = requests.get(feched_message.attachments[0].url, stream=True).raw
        img = np.asarray(bytearray(resp.read()), dtype="uint8")

        img = cv2.imdecode(img, cv2.IMREAD_COLOR)

        img_bytes = cv2.imencode('.jpg', img,(cv2.IMWRITE_JPEG_QUALITY, quality))[1]

        bio = io.BytesIO(img_bytes)

        img_file = discord.File(fp=bio,filename="satujin.jpg")

        await ctx.send(file=img_file)


async def setup(bot):
    await bot.add_cog(Gabigabi(bot))