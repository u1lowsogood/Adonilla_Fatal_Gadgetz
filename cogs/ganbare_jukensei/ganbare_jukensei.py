from discord.ext import commands
import random
import numpy as np
import cv2
import puttext
import datetime
import locale

class Ganbare(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["頑張れ受験生","がんばれ受験生","がんばれじゅけんせい","ganbarejukensei","頑張れ"])
    def ganbare_jukensei(self, ctx):

        locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')

        era = random.choice(["大正","昭和","平成","令和"])
        erayear = random.randint(0,500)

        year = random.randint(-2000,2000)
        month = random.randint(1,12)
        day = random.randint(1,29)

        hour = random.randint(1,24)
        minute = random.randint(1,60)
        second = random.randint(1,60)
        
        time = datetime.datetime(year, month, day, hour=hour, minute=minute, second=second, microsecond=0, tzinfo=None)
        
        sendtxt_1 = era + str(erayear) + "年度 大学入学共通テスト（新テスト）開始時刻"
        sendtxt_2 = time.strftime("%Y年%m月%d日（%a）%p%I%Mまで") 
        sendtxt_4 = "がんばれ受験生！"

        img = np.zeros((500,255,3), np.uint8)
        puttext.cv2_putText(img, sendtxt_1, (0,0), "MEIRYO.TTC", 20, (255,255,255), anchor="lt")

async def setup(bot):
    await bot.add_cog(Ganbare(bot))