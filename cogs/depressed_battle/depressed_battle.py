from discord.ext import commands
import discord.ext.commands
import discord

import psycopg2
from psycopg2.extras import DictCursor

from transformers import pipeline, AutoModelForSequenceClassification, BertJapaneseTokenizer,BertTokenizer, BertForSequenceClassification

import torch
from datetime import datetime

import discord.ext

class DepressedBattle(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        # 精度微妙だったので他使う
        #self.classifier = pipeline(
        #    model="lxyuan/distilbert-base-multilingual-cased-sentiments-student", 
        #    top_k=None) 
        
        self.model = AutoModelForSequenceClassification.from_pretrained('koheiduck/bert-japanese-finetuned-sentiment') 
        self.tokenizer = BertJapaneseTokenizer.from_pretrained('tohoku-nlp/bert-base-japanese-whole-word-masking')
        self.classifier = pipeline("sentiment-analysis",model=self.model,tokenizer=self.tokenizer)

        self.rank_table = [
                ["👑 LEGEND級", 97, "精神科の受診を検討して下さい。"],
                ["🔱 SS級", 95, "鬱病キングです！　医師の診断を受け、ただちに健常者になりましょう！"],
                ["🌟 S級", 90, "輝く鬱病の星です！　常人より寿命が30年短くなると思われます！"],
                ["⭐ A級", 85, "鬱病の星です！　専門家のカウンセリングが必要でしょう！"],
                ["🌼 B級", 70, "花丸印の鬱です！　まだ命の電話で助かります！"],
                ["🥀 C級", 60, "軽度の鬱です！　この位の気の落ち込みは病の範疇に含まれません。"],
                ["🌚 D級", 40, "ファッション鬱です！　鬱病というステータスを得るにはちょうど良いラインかもしれませんねｗ"],
                ["🥶 E級", 0, "健常者過ぎます！　ある意味、精神異常者と言えるかもしれません……ｗ"],
            ]

    # メッセージを全部SQLに放り込む
    @commands.Cog.listener(name="on_message")
    async def emotioninsert(self,msg : discord.Message):
        text = msg.content
        if text == "":
            return
        emotions = self.emotion_detector(text)
        self.sqlinsert(msg.author.id, emotions["POSITIVE"], emotions["NEGATIVE"], emotions["NEUTRAL"])

    @commands.command(aliases=["howmuchdepressed","utsudo"])
    async def utusokutei(self, ctx: discord.ext.commands.Context):
        if ctx.message.reference == None:
            await ctx.channel.send("この機能は返信といっしょに使用してね♪（詳細：/utuhelp）")
            return

        targettxt = await ctx.message.channel.fetch_message(ctx.message.reference.message_id)
        targettxt = targettxt.content
        detected_emotions = self.emotion_detector(targettxt)

        rank_result = self.get_rank(detected_emotions["NEGATIVE"])

        sendtext = "```md\n# 【この発言の鬱レベルは……？】\n```\n"
        sendtext += "# ＜ __"+rank_result[0]+"__ ＞\n"
        sendtext += "# :skull: 鬱度:"+str(detected_emotions["NEGATIVE"])+"%\n"
        sendtext += ":heart: 幸福度 "+str(detected_emotions["POSITIVE"])+"%\n"
        sendtext += ":neutral_face: 普通度 "+str(detected_emotions["NEUTRAL"])+"%\n"
        sendtext += "```\nコメント：\n"+rank_result[2]+"\n```"
        
        await ctx.channel.send(sendtext)

    def get_rank(self,negative_rate):
        for rank in self.rank_table:
            if rank[1] <= negative_rate:
                return rank

    def emotion_detector(self,text):
        inputs = self.tokenizer(text, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model(**inputs)

        logits = outputs.logits
        probs = torch.softmax(logits, dim=-1)

        probabilities = probs[0].cpu().numpy()

        labels = ['NEUTRAL', 'NEGATIVE', 'POSITIVE']

        result = {}

        for label, prob in zip(labels, probabilities):
            prob *= 100
            result[label] = round(prob,2)

        return result
    
    @commands.command()
    async def uturank(self, ctx, total=None):
        with psycopg2.connect(user=self.bot.sqluser, password=self.bot.sqlpassword, host="localhost", port="5432", dbname="depressed_battle") as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("""
                SELECT 
                    patient_uuid,
                    AVG(positive_rate) AS avg_positive_rate,
                    AVG(negative_rate) AS avg_negative_rate,
                    AVG(neutral_rate) AS avg_neutral_rate
                FROM depressed
                WHERE patient_uuid <> %s
                GROUP BY patient_uuid
                ORDER BY avg_negative_rate DESC
                LIMIT 5
            """,("1144055461247717506",))

                rows = cur.fetchall()
                
                sendtxt = "```md\n# 【不幸度総合ランキング】\nこのサーバーで最も不幸なのは……！？```\n"
                
                for i, row in enumerate(rows):

                    member = await ctx.guild.fetch_member(row["patient_uuid"])
                    membername =  member.name if member.nick == None else member.nick

                    sendtxt += f"## __{i+1}位.  {membername}__  (鬱度：{round(row['avg_negative_rate'],2)}%)\n"
                    sendtxt += f"**＜ {self.get_rank(row['avg_negative_rate'])[0]} ＞**\n"
                
                await ctx.channel.send(sendtxt)

    @commands.command()
    async def utuhelp(self, ctx :discord.ext.commands.Context):
        sendtxt = "```md\n# 【鬱感情測定ツール：使い方】\nAIがあなたの感情を文章から自動認識します！```"
        sendtxt +="```\n/utuhelp\nコマンドの使い方を表示するぞ！ \
        \n\n/uturank\nこのサーバーでの鬱ランキングを表示するぞ！ \
        \n\n/utuprofile\nあなたの今までの発言の鬱度の平均を表示するぞ！ \
        \n\n/utusokutei\n返信と一緒に使用すると、返信元の文章の鬱度合いを測定できるぞ！ \
        \n\n/utuserver\nこのサーバー全体の鬱度合いを表示するぞ！```"
        sendtxt += "```\n使用AIモデル：\nkoheiduck/bert-japanese-finetuned-sentiment\
        \nトークナイザー：\ntohoku-nlp/bert-base-japanese-whole-word-masking```"

        await ctx.channel.send(sendtxt)

    @commands.command()
    async def utuserver(self, ctx :discord.ext.commands.Context):
        with psycopg2.connect(user=self.bot.sqluser, password=self.bot.sqlpassword, host="localhost", port="5432", dbname="depressed_battle") as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute("""
                    SELECT 
                        AVG(positive_rate) AS avg_positive_rate,
                        AVG(negative_rate) AS avg_negative_rate,
                        AVG(neutral_rate) AS avg_neutral_rate
                    FROM depressed
                    WHERE patient_uuid <> %s;
                """,("1144055461247717506",))
                
                row = cur.fetchone()
                
                sendtxt = f"```md\n# 【このサーバーの平均精神健康度は……】\n```\n"
                sendtxt += f"# :skull:鬱度：{round(row['avg_positive_rate'],2)}%\n"
                sendtxt += f":heart:幸福度：{round(row['avg_positive_rate'],2)}%\n"
                sendtxt += f":neutral_face:普通度：{round(row['avg_positive_rate'],2)}%\n\n"
                sendtxt += f"```\nです！```\n"

                await ctx.channel.send(sendtxt)

    @commands.command()
    async def utuprofile(self, ctx :discord.ext.commands.Context):
        uuid = str(ctx.message.author.id)
        sql = """
            WITH ranked_rates AS (
                SELECT 
                    patient_uuid,
                    AVG(positive_rate) AS avg_positive_rate,
                    AVG(negative_rate) AS avg_negative_rate,
                    AVG(neutral_rate) AS avg_neutral_rate,
                    RANK() OVER (ORDER BY AVG(positive_rate) DESC) AS rank
                FROM depressed
                WHERE patient_uuid <> %s
                GROUP BY patient_uuid
            )
            SELECT 
                patient_uuid,
                avg_positive_rate,
                avg_negative_rate,
                avg_neutral_rate,
                rank
            FROM ranked_rates
            WHERE patient_uuid = %s AND patient_uuid <> %s;
        """
        with psycopg2.connect(user=self.bot.sqluser, password=self.bot.sqlpassword, host="localhost", port="5432", dbname="depressed_battle") as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(sql, ("1144055461247717506",uuid,"1144055461247717506"))
                row = cur.fetchone()
                
                sendtxt = "```md\n# 【あなたの総合不幸度順位】\nあなたの今までの発言の不幸度合いは……？```\n"

                member = await ctx.guild.fetch_member(row["patient_uuid"])
                membername =  member.name if member.nick == None else member.nick

                rank_degree = self.get_rank(row['avg_negative_rate'])

                if row:
                    sendtxt += f"## ・__{membername}__ （{row['rank']}位）\n"
                    sendtxt += f"**💀鬱度：{round(row['avg_negative_rate'],2)}%**\n"
                    sendtxt += f"❤️幸福度：{round(row['avg_positive_rate'],2)}%\n"
                    sendtxt += f"😐普通度：{round(row['avg_neutral_rate'],2)}%\n\n"
                    sendtxt += f"```md\n# 【あなたの総合不幸ランクは……】\n```\n"
                    sendtxt += f"**＜{rank_degree[0]}＞**\n\n"
                    sendtxt += f"```\nコメント：\n{rank_degree[2]}\n```"
                else:
                    sendtxt += f"## __{membername}__ （？位）\n"
                    sendtxt += f"**データなし**"

                await ctx.channel.send(sendtxt)

    def sqlinsert(self, author_id, positive_rate, negative_rate, neutral_rate):
        today = datetime.now().date()
        author_id = str(author_id)
        try:
            with psycopg2.connect(user=self.bot.sqluser, password=self.bot.sqlpassword, host="localhost", port="5432", dbname="depressed_battle") as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT positive_rate, negative_rate, neutral_rate 
                        FROM depressed 
                        WHERE patient_uuid = %s AND created_at = %s
                    """, (author_id, today))
                    
                    result = cur.fetchone()
                    
                    if result:
                        current_positive, current_negative, current_neutral = result
                        new_positive = (current_positive + positive_rate) / 2
                        new_negative = (current_negative + negative_rate) / 2
                        new_neutral = (current_neutral + neutral_rate) / 2

                        cur.execute("""
                            UPDATE depressed 
                            SET positive_rate = %s, negative_rate = %s, neutral_rate = %s
                            WHERE patient_uuid = %s AND created_at = %s
                        """, (new_positive, new_negative, new_neutral, author_id, today))
                    else:
                        cur.execute("""
                            INSERT INTO depressed (
                                patient_uuid, positive_rate, negative_rate, neutral_rate, created_at
                            ) VALUES (%s, %s, %s, %s, %s)
                        """, (author_id, positive_rate, negative_rate, neutral_rate, today))
                    
                    conn.commit()
                    #print(f"sql updated or inserted for {author_id}")
        except Exception as e:
            print(f"something happened: {e}")

async def setup(bot):
    await bot.add_cog(DepressedBattle(bot))