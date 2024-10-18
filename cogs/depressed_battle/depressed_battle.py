from discord.ext import commands
import discord
import psycopg2
import discord.ext.commands
from transformers import pipeline

import discord.ext

class DepressedBattle(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.classifier = pipeline(
            model="lxyuan/distilbert-base-multilingual-cased-sentiments-student", 
            top_k=None)
        self.emodict = {"Negative":"鬱","Positive":"躁","Neutral":"一般"}

        def sqlinsert(self,senryu):
            sql = """
                insert into depressedbattle(
                    author_uid
                    ,rate
                )values(
                    %s
                    ,%s
                )
            """
            try:
                with psycopg2.connect(user=self.bot.sqluser, password=self.bot.sqlpassword,host="localhost", port="5432", dbname="depressedbattle") as conn:
                    with conn.cursor() as cur:
                        cur.execute(sql, (self.replyto.author.id, senryu))
                        #print(f"sql inserted: {senryu}")
            except:
                print("something happen w")

    @commands.Cog.listener(name="on_message")
    async def senryu_verdict(self,msg : discord.Message):
        if "/" in msg.content:
            return
        
    @commands.command(name="ranking",aliases=["鬱病ランキング","uturank","鬱ランク"])
    async def utsubyouranking(self, ctx, total=None):
        #await ctx.channel.send(send)
        pass

    @commands.command(aliases=["howmuchdepressed"])
    async def utusokutei(self, ctx: discord.ext.commands.Context):
        if ctx.message.reference != None:

            targettxt = await ctx.message.channel.fetch_message(ctx.message.reference.message_id).content
            detected = self.emotionDetector(targettxt)

            rank_table = [
                ["👑 LEGEND級", 97],
                ["🔱 SS級", 95],
                ["🌟 S級", 90],
                ["⭐ A級", 85],
                ["🌼 B級", 70],
                ["🥀 C級", 60],
                ["🌚 D級", 40],
                ["🥶 E級", 0],
            ]
            result = rank_table[0]

            for rank in rank_table:
                if rank[1] <= detected["Negative"]:
                    result = rank
                    break

            sendtext = \
                f"```md\n \
                # 【この発言の鬱レベルは……？】\n \
                ```\n \
                # {result[0]} （鬱度 {detected["Negative"]}%）\n \
                ```\n \
                普通：{detected["Neutral"]}% \n \
                喜：{detected["Positive"]:}% \n \
                ```"



        
    def emotionDetector(self,text):
        classified = self.classifier(text)[0]
        result = {}
        for sentiment in classified:
            label = sentiment['label']
            score = sentiment['score'] * 100
            result[label.capitalize()] = round(score,2)
        return result

async def setup(bot):
    await bot.add_cog(DepressedBattle(bot))