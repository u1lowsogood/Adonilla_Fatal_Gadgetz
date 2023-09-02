from discord.ext import commands
import numpy as np
from lib import puttext
import cv2
import io
import requests
import discord
import random

class Noconico(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.comments = [
            "いつもの",
            "まるで実家のような安心感",
            "キンタマ",
            "ひじき",
            "ネオナチ",
            "いつもの",
            "安倍晋三",
            "戊辰戦争",
            "生きがい",
            "いきがい",
            "リスポーン地点",
            "何か書いとけ",
            "おまたせ",
            "やったぜ",
            "これはひどい",
            "生存確認",
            "恥を売る",
            "もう実家",
            "親の顔より見た画像",
            "ワクワクさん"]

    @commands.command(aliases=["赤字","あかじ","akazi"])
    async def akaji(self, ctx, *args):
        if ctx.message.reference == None:
            await ctx.send("このコマンドは返信\n # と一緒に\n # 利用してみてねｗ←ｗ")
            return
        
        if len(args) == 0:
            args = random.sample(self.comments,7)
        else:
            args = list(args)

        for i, arg in enumerate(args):
            newarg = ""
            spaceamount = random.randint(0,2)
            for moji in arg:
                newarg += moji+spaceamount*"　"
            args[i] = newarg.lstrip()
        
        feched_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if feched_message.attachments == []:
            await ctx.send("返\n信\n# 先のメ\nッセージは画像である必要が……\n # ある")
            return
        
        resp = requests.get(feched_message.attachments[0].url, stream=True).raw
        img = np.asarray(bytearray(resp.read()), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)

        height, width = img.shape[-3:-1]
        center = int(width / 2)
        fontsize = int(width / 15)

        for i, arg in enumerate(args):
            puttext.cv2_putText(img, arg, (center, fontsize+(i*fontsize)), "C:\\Windows\\Fonts\\msgothic.ttc", fontsize, (0,0,255), anchor="mm")

        img_bytes = cv2.imencode('.png', img)[1].tobytes()

        bio = io.BytesIO(img_bytes)

        img_file = discord.File(fp=bio,filename="satujin.png")

        await ctx.send(file=img_file)


async def setup(bot):
    await bot.add_cog(Noconico(bot))