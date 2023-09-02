from discord.ext import commands
import random
import numpy as np
import cv2
import PIL
import datetime
import locale
import requests

class Noconico(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["赤字","あかじ","akazi"])
    async def akaji(self, ctx):
        if ctx.message.reference == None:
            await ctx.send("このコマンドは返信\n # と一緒に\n # 利用してみてねｗ←ｗ")
            return
        
        feched_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if feched_message.attachments == []:
            await ctx.send("返\n信\n# 先のメ\nッセージは画像である必要が……\n # ある")
            return
        
        resp = requests.get(feched_message.attachments[0].url, stream=True).raw
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        


async def setup(bot):
    await bot.add_cog(Noconico(bot))