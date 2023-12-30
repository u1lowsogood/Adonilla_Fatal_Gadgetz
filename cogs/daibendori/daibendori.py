from discord.ext import commands
import numpy as np
from lib import puttext
import cv2
import io
import discord
import random

class Daibendori(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["dbd","代弁鳥"])
    async def daibendori(self,ctx,*,text):
        putpoint = [["db1.png",210,430],["db2.png",215,400],["db3.png",207,380],["db4.png",210,400]]

        choiced = random.choice(putpoint)

        img = cv2.imread("./cogs/daibendori/pics/"+choiced[0])
        split_text = [text[i:i+10] for i in range(0, len(text), 10)]
        tlen = len(split_text)

        for i,t in enumerate(split_text):
            puttext.cv2_putText(img, t, (choiced[1],choiced[2]-tlen*17+(i*34)+17), "./cogs/amanda/NotoSansJP-Regular.ttf", 34, (0,0,0), anchor="mm")

        img_bytes = cv2.imencode('.png', img)[1].tobytes()
        bio = io.BytesIO(img_bytes)
        img_file = discord.File(fp=bio,filename="代弁鳥.png")

        await ctx.send(file=img_file)
        await ctx.send("と言っているよ")

async def setup(bot):
    await bot.add_cog(Daibendori(bot))