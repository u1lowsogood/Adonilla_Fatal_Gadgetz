from discord.ext import commands
import numpy as np
from lib import puttext
import cv2
import io
import discord
import random
import emoji
import json

class Yugamismile(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.loc = "./cogs/yugamismile/smile.png"
        
        dir = "./cogs/yugamismile/emojishortcuts.json"
        with open(dir, mode="rt", encoding="utf-8") as f:
            self.json_dict = json.load(f)

    def emoji2smile(self, input):
        for child in self.json_dict:
            input = input.replace(child["emoji"],child["shortcuts"][0])
        return input
    
    async def sendsmily(self, ctx, location, input, rotate):

        face = self.emoji2smile(input)

        img = cv2.imread(self.loc)

        puttext.cv2_putText(img, face, location, "./cogs/amanda/NotoSansJP-Regular.ttf", 90, (0,0,0), anchor="mm",rotate=rotate)

        img_bytes = cv2.imencode('.png', img)[1].tobytes()
        bio = io.BytesIO(img_bytes)
        img_file = discord.File(fp=bio,filename="歪み笑顔.png")

        await ctx.send(file=img_file)


    @commands.command(aliases=[":}","：｝"])
    async def yugamismile_rotated(self,ctx,*,face):
        await self.sendsmily(ctx,(130,130),face,True)

    @commands.command(aliases=["ﾂ","ツ"])
    async def yugamismile(self,ctx,*,face):
        await self.sendsmily(ctx,(130,130),face,False)



async def setup(bot):
    await bot.add_cog(Yugamismile(bot))