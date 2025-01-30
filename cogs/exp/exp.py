from discord.ext import commands
import cv2
import io
import discord

class EXP(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.expsystem = self.bot.system.expsystem

    @commands.command()
    async def exptest(self,ctx,sex:str="セックス",amanda:str="アマンダ",hardfuck:str="ハードファック"):
        text = sex + "爆弾" + amanda + "は" + hardfuck

        img = cv2.imread("./cogs/amanda/amanda_base.png")

        img_bytes = cv2.imencode('.png', img)[1].tobytes()
        bio = io.BytesIO(img_bytes)
        img_file = discord.File(fp=bio,filename="amanda.png")

        await ctx.send(file=img_file)

async def setup(bot):
    await bot.add_cog(EXP(bot))