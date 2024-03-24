
import discord
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw
import cv2
import io
import random

class FakeGoogle(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["検索","kensaku","google","gg"])
    async def search(self, ctx, *searchwords_input_array):

        searchwords = ' '.join(searchwords_input_array)

        googlepic = Image.open("cogs/fakegoogle/google.png")
        picDraw = ImageDraw.Draw(googlepic)

        font = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 20)
        picDraw.text((215,38), searchwords, font=font, fill=('#000000'))

        output = io.BytesIO()
        googlepic.save(output, format='PNG')
        image_byte = io.BytesIO(output.getvalue())

        img_file = discord.File(fp=image_byte,filename="search.png")

        await ctx.channel.send(file=img_file)

async def setup(bot):
    await bot.add_cog(FakeGoogle(bot))