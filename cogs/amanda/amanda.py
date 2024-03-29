from discord.ext import commands
import numpy as np
from lib import puttext
import cv2
import io
import discord

class Amanda(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["アマンダ","あまんだ","amannda"])
    async def amanda(self,ctx,sex:str="セックス",amanda:str="アマンダ",hardfuck:str="ハードファック"):
        text = sex + "爆弾" + amanda + "は" + hardfuck

        img = cv2.imread("./cogs/amanda/amanda_base.png")
        puttext.cv2_putText(img, text, (340, 380), "./cogs/amanda/NotoSansJP-Regular.ttf", 34, (255,255,255), anchor="mm")

        img_bytes = cv2.imencode('.png', img)[1].tobytes()
        bio = io.BytesIO(img_bytes)
        img_file = discord.File(fp=bio,filename="amanda.png")

        await ctx.send(file=img_file)

async def setup(bot):
    await bot.add_cog(Amanda(bot))