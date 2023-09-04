from discord.ext import commands
import random

class Ninti(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["認知の歪みガチャ","認知","にんち","ninchi","ninnchi","ninnti"])
    async def ninch(self, ctx):
    #認知の歪みガチャ
    #DBはユーザIDと最終投稿日時 獲得したガチャの情報を持つ
    #最終投稿日時からn時間後に再度ガチャを引ける
    # コンプリートすると「鬱病」or「殺人者」を獲得
    # 獲得した認知の歪み毎に起因した複数のエピソードが紐づいており
    # コンプ後自殺or他殺で人生ストーリーが綴られ、DBがリセット
        await ctx.send("a")

async def setup(bot):
    await bot.add_cog(Ninti(bot))
    

