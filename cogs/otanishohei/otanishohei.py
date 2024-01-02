from discord.ext import commands
import numpy as np
from lib import puttext
import cv2
import io
import discord

class OtaniShohei(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["大谷翔平","os"])
    async def otanishohei(self,ctx,hour:str = "12"):


        img = cv2.imread("./cogs/otanishohei/OS.png")

        move = []
        for i in range(4):
            move.extend([(-i,-i),(-i,i),(i,-i),(i,i)])

        hour = hour[::-1]

        for i, h in enumerate(hour):
            for m in move:
                puttext.cv2_putText(img, h, (155-(i*36) + m[0], 385+m[1]), "./cogs/otanishohei/BIZUDPGothic-Bold.ttf", 50, (255,255,255), anchor="lt")
            puttext.cv2_putText(img, h, (155-(i*36), 385), "./cogs/otanishohei/BIZUDPGothic-Regular.ttf", 50, (186,209,225), anchor="lt")

        img_bytes = cv2.imencode('.png', img)[1].tobytes()
        bio = io.BytesIO(img_bytes)
        img_file = discord.File(fp=bio,filename="shohei.png")

        await ctx.send(file=img_file)

async def setup(bot):
    await bot.add_cog(OtaniShohei(bot))