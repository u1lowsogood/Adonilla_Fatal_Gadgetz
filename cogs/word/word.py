
from discord.ext import commands
import urllib3
from bs4 import BeautifulSoup
import random

class Word(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["英単語","eitango","単語","tango"])
    async def word(self, ctx, eitango):

        url = 'https://ejje.weblio.jp/content/' + eitango

        http = urllib3.PoolManager()

        instance = http.request('GET', url)
        soup = BeautifulSoup(instance.data, 'html.parser')

        rank = soup.find("span",class_="content-explanation ej")
        
        if rank == None:
            await ctx.channel.send("```md\n* 英単語「" + eitango + "」の検索結果が見つかりませんでした・・・\n```")
        else:
            await ctx.channel.send("```md\n#英単語「" + eitango + "」の主な意味は・・・\n" + rank.text.strip() + "```")

async def setup(bot):
    await bot.add_cog(Word(bot))