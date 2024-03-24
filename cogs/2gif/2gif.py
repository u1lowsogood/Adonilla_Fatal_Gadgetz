
import discord
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw
import cv2
import io
import random

class GifConverter(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["2gif"])
    async def gifconverter(self, ctx, *searchwords_input_array):

        latestmessage = historykun[1]

        download_vid(latestmessage.attachments[0].url, latestmessage.attachments[0].filename)

        exepath = "C:/ffmpeg-20200715-a54b367-win64-static/bin/ffmpeg.exe"
        inputpath = "D:/いろいろあるやつ/VSCode/workspace/AdonillaUtilityToolz/2gif/" + latestmessage.attachments[0].filename
        outputpath = "D:/いろいろあるやつ/VSCode/workspace/AdonillaUtilityToolz/2gif/" + latestmessage.attachments[0].filename + ".output.gif"

        if inputpath.split(".")[-1] == "mp4" or inputpath.split(".")[-1] == "mov" or inputpath.split(".")[-1] == "gif":
            if "," not in message.content:
                subprocess.run(exepath+" -i "+inputpath+" -filter_complex \"[0:v] fps=10,scale=400:-1,split [a][b];[a] palettegen [p];[b][p] paletteuse=dither=none\" "+outputpath, shell=True)
            else:
                subprocess.run(exepath+" -i "+inputpath+" -filter_complex \"[0:v] fps="+message.content.split(",")[1]+",scale="+message.content.split(",")[2]+":-1,split [a][b];[a] palettegen [p];[b][p] paletteuse=dither=none\" "+outputpath,shell=True)
        else:
            subprocess.run(exepath+" -i "+inputpath+" -filter_complex \"split [a][b];[a] palettegen [p];[b][p] paletteuse=dither=none\" "+outputpath, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            await message.channel.send(file=discord.File(outputpath))
            await message.channel.send("これで満足か？ｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗ")
        except discord.errors.HTTPException:
            await message.channel.send("サイズデカすぎンが与ｗｗｗｗｗｗ2gif,[FPS],[SIZE]")

        print(inputpath)
        subprocess.run("rm " + inputpath,shell=True)
        subprocess.run("rm " + outputpath,shell=True)

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
    await bot.add_cog(GifConverter(bot))