import discord
from discord.ext import commands
import random
import re
import datetime

class RandomMusic(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
        self.channel = self.bot.get_channel(745417276919906305)
        self.limit = 600

    def random_datetime(self, start_datetime, end_datetime):
        time_difference = end_datetime - start_datetime
        random_time_difference = datetime.timedelta(seconds=random.randint(0, int(time_difference.total_seconds())))
        random_datetime = start_datetime + random_time_difference
        return random_datetime

    @commands.command(aliases=["ram","ランダム音楽"])
    async def randommusic(self, ctx : commands.Context, member : discord.Member = None):

        time = 0
        searching = await ctx.send(f"検索中……({time}/{self.limit})")

        while(True):
            oldest_message = [message async for message in self.channel.history(limit=3,oldest_first=True)][0]
            random_datatime = self.random_datetime(oldest_message.created_at, ctx.message.created_at)
        
            async for message in self.channel.history(around=random_datatime):
                time += 1
                if member != None and message.author != member:
                    continue

                url_list = re.findall(self.pattern, message.content)
                if len(url_list) == 0:
                    continue
                else:
                    await searching.delete()
                    await ctx.send(random.choice(url_list))
                    return
                
            await searching.edit(content=f"検索中……({time}/{self.limit})")
                
            if time > 500:
                await searching.edit(content="曲を見つけられませんでした……ｗ\n（ランダムに検索しているので運が悪い可能性もあるｗ\n（その場合は再トライしてみてねｗ））")
                return




async def setup(bot):
    await bot.add_cog(RandomMusic(bot))