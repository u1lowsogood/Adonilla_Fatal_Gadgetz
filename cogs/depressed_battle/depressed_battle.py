from discord.ext import commands
import discord.ext.commands
import discord
import discord.ext

import psycopg2
from psycopg2.extras import DictCursor

from transformers import pipeline, AutoModelForSequenceClassification, BertJapaneseTokenizer,BertTokenizer, BertForSequenceClassification
import torch

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.font_manager as fm
import japanize_matplotlib

import emoji
from datetime import datetime, timedelta
import io
import re

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

        self.rank_table_sokutei = [
                ["👑 LEGEND級", 97, "精神科の受診を検討して下さい。"],
                ["🔱 SS級", 95, "鬱病キングです！　医師の診断を受け、ただちに健常者になりましょう！"],
                ["🌟 S級", 90, "輝く鬱病の星です！　常人より寿命が30年短くなると思われます！"],
                ["⭐ A級", 85, "鬱病の星です！　専門家のカウンセリングが必要でしょう！"],
                ["🌼 B級", 70, "花丸印の鬱です！　まだ命の電話で助かります！"],
                ["🥀 C級", 60, "軽度の鬱です！　この位の気の落ち込みは病の範疇に含まれません。"],
                ["🌚 D級", 40, "ファッション鬱です！　鬱病というステータスを得るにはちょうど良いラインかもしれませんねｗ"],
                ["🥶 E級", 0, "健常者過ぎます！　ある意味、精神異常者と言えるかもしれません……ｗ"],
            ]

        self.rank_table_profile = [
                ["👑 LEGEND級", 60, "精神科の受診を検討して下さい。"],
                ["🔱 SS級", 55, "鬱病キングです！　医師の診断を受け、ただちに健常者になりましょう！"],
                ["🌟 S級", 50, "輝く鬱病の星です！　常人より寿命が30年短くなると思われます！"],
                ["⭐ A級", 45, "鬱病の星です！　専門家のカウンセリングが必要でしょう！"],
                ["🌼 B級", 40, "花丸印の鬱です！　まだ命の電話で助かります！"],
                ["🥀 C級", 35, "軽度の鬱です！　この位の気の落ち込みは病の範疇に含まれません。"],
                ["🌚 D級", 30, "ファッション鬱です！　鬱病というステータスを得るにはちょうど良いラインかもしれませんねｗ"],
                ["🥶 E級", 0, "健常者過ぎます！　ある意味、精神異常者と言えるかもしれません……ｗ"],
            ]

    # メッセージを全部SQLに放り込む
    @commands.Cog.listener(name="on_message")
    async def emotioninsert(self,msg : discord.Message):
        text = msg.content
        if text == "" or "/" in text:
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

        rank_result = self.get_rank(detected_emotions["NEGATIVE"],False)

        sendtext = "```md\n# 【この発言の鬱レベルは……？】\n```\n"
        sendtext += "# ＜ __"+rank_result[0]+"__ ＞\n"
        sendtext += "# :skull: 鬱度:"+str(detected_emotions["NEGATIVE"])+"%\n"
        sendtext += ":heart: 幸福度 "+str(detected_emotions["POSITIVE"])+"%\n"
        sendtext += ":neutral_face: 普通度 "+str(detected_emotions["NEUTRAL"])+"%\n"
        sendtext += "```\nコメント：\n"+rank_result[2]+"\n```"
        
        await ctx.channel.send(sendtext)

    def get_rank(self,negative_rate,profilerank):
        ranktable = self.rank_table_profile if profilerank else self.rank_table_sokutei
        for rank in ranktable:
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
    async def uturank(self, ctx, graph="weekly"):
        if graph == "total":
            with psycopg2.connect(user=self.bot.sqluser, password=self.bot.sqlpassword, host="localhost", port="5432", dbname="depressed_battle") as conn:
                with conn.cursor(cursor_factory=DictCursor) as cur:
                    cur.execute("""
                        SELECT 
                            patient_uuid,
                            SUM(positive_rate * amount) / SUM(amount) AS weighted_avg_positive_rate,
                            SUM(negative_rate * amount) / SUM(amount) AS weighted_avg_negative_rate,
                            SUM(neutral_rate * amount) / SUM(amount) AS weighted_avg_neutral_rate
                        FROM depressed
                        WHERE patient_uuid <> %s
                        GROUP BY patient_uuid
                        ORDER BY weighted_avg_negative_rate DESC
                        LIMIT 5
                    """, ("1144055461247717506",))

                    rows = cur.fetchall()
                    
                    sendtxt = "```md\n# 【不幸度総合ランキング】\nこのサーバーで最も不幸なのは……！？```\n"
                    
                    for i, row in enumerate(rows):

                        member = await ctx.guild.fetch_member(row["patient_uuid"])
                        membername =  member.name if member.nick == None else member.nick

                        sendtxt += f"## __{i+1}位.  {membername}__  (鬱度：{round(row['weighted_avg_negative_rate'],2)}%)\n"
                        sendtxt += f"**＜ {self.get_rank(row['weighted_avg_negative_rate'],True)[0]} ＞**\n"
                    
                    await ctx.channel.send(sendtxt)

        elif graph == "week" or graph == "weekly":
            with psycopg2.connect(user=self.bot.sqluser, password=self.bot.sqlpassword, host="localhost", port="5432", dbname="depressed_battle") as conn:
                with conn.cursor(cursor_factory=DictCursor) as cur:

                    today = datetime.now().date()
                    start_date = today - timedelta(days=7)

                    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

                    cur.execute("""
                        SELECT 
                            patient_uuid,
                            SUM(negative_rate * amount) / SUM(amount) AS weighted_avg_negative_rate
                        FROM depressed
                        WHERE patient_uuid <> %s AND created_at BETWEEN %s AND %s
                        GROUP BY patient_uuid
                        ORDER BY weighted_avg_negative_rate DESC
                        LIMIT 5
                    """, ("1144055461247717506", start_date, today))
                    top5_users = cur.fetchall()
                    
                    plt.figure(figsize=(12, 8))
                    
                    for i,user in enumerate(top5_users,start=1):
                        uuid = user["patient_uuid"]
                        cur.execute("""
                            SELECT
                                created_at,
                                negative_rate
                            FROM depressed
                            WHERE patient_uuid = %s AND created_at BETWEEN %s AND %s
                            ORDER BY created_at ASC;
                        """, (uuid, start_date, today))
                        
                        user_data = cur.fetchall()
                        dates = [row["created_at"] for row in user_data]
                        negative_rates = [row["negative_rate"] for row in user_data]

                        # 平均を計算してプロット用リストに格納
                        if dates:  # データが存在する場合
                            avg_negative_rate = sum(negative_rates) / len(negative_rates)
                            plt.axhline(y=avg_negative_rate, color=colors[i-1], linestyle='--', alpha=0.4)

                        member = await ctx.guild.fetch_member(int(uuid))
                        membername =  member.name if member.nick == None else member.nick
                        membername = emoji.get_emoji_regexp().sub(u'', membername)

                        plt.plot(dates, negative_rates, color=colors[i-1], marker="o", markersize=8, label=f"{i}位：{member}")

                    date_format = JapaneseDateFormatter('%m月%d日')
                    plt.gca().xaxis.set_major_formatter(date_format)
                        
                    # プロット設定
                    plt.title(f"近々一週間のランク ～THE 鬱遷移～",fontsize=25)
                    plt.xlabel("日付",fontsize=20)
                    plt.ylabel("鬱率",fontsize=20)
                    plt.legend(title="患者",fontsize=20)
                    plt.xticks(dates[::1],rotation=45,fontsize=20)
                    plt.tight_layout()

                    bio = io.BytesIO()
                    plt.savefig(fname=bio, format="png")
                    bio.seek(0) 
                    img_file = discord.File(fp=bio,filename="graph.png")
                    await ctx.send("``/uturank total``で全期間のランキングを表示",file=img_file)
                    plt.close()

    @commands.command()
    async def utuhelp(self, ctx :discord.ext.commands.Context):
        sendtxt = "```md\n# 【鬱感情測定ツール：使い方】\nAIがあなたの感情を文章から自動認識します！```"
        sendtxt +="```\n/utuhelp\nコマンドの使い方を表示するぞ！ \
        \n\n/uturank\nこのサーバーでの鬱ランキングを表示するぞ！ \
        \n\n/utuprofile\nあなたの今までの発言の鬱度の平均を表示するぞ！返信先のユーザーも見れるぞ！” \
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
                        SUM(positive_rate * amount) / SUM(amount) AS avg_positive_rate,
                        SUM(negative_rate * amount) / SUM(amount) AS avg_negative_rate,
                        SUM(neutral_rate * amount) / SUM(amount) AS avg_neutral_rate
                    FROM depressed
                    WHERE patient_uuid <> %s;
                """,("1144055461247717506",))
                
                row = cur.fetchone()
                
                sendtxt = f"```md\n# 【このサーバーの平均精神健康度は……】\n```\n"
                sendtxt += f"# :skull:鬱度：{round(row['avg_negative_rate'],2)}%\n"
                sendtxt += f":heart:幸福度：{round(row['avg_positive_rate'],2)}%\n"
                sendtxt += f":neutral_face:普通度：{round(row['avg_neutral_rate'],2)}%\n\n"
                sendtxt += f"```\nです！```\n"

                await ctx.channel.send(sendtxt)

                today = datetime.now().date()
                start_date = today - timedelta(days=7)

                sql_fetch_weekly_rate = """
                SELECT
                    created_at,
                    SUM(negative_rate * amount) / SUM(amount) AS all_negative_rate,
                    SUM(positive_rate * amount) / SUM(amount) AS all_positive_rate
                FROM depressed
                WHERE patient_uuid <> %s AND created_at BETWEEN %s AND %s
                GROUP BY created_at
                ORDER BY created_at ASC;
                """

                cur.execute(sql_fetch_weekly_rate,("1144055461247717506",start_date,today))
                server_data = cur.fetchall()

                dates = [row["created_at"] for row in server_data]
                negative_rates = [row["all_negative_rate"] for row in server_data]
                positive_rates = [row["all_positive_rate"] for row in server_data]

                plt.plot(dates, negative_rates, marker="o", markersize=8, label=f"鬱")
                plt.plot(dates, positive_rates, marker="o", markersize=8, label=f"喜")

                date_format = JapaneseDateFormatter('%m月%d日')
                plt.gca().xaxis.set_major_formatter(date_format)
                # プロット設定
                plt.title(f"このサーバーの近々一週間の鬱遷移",fontsize=20)
                plt.legend(fontsize=20)
                plt.xlabel("日付",fontsize=15)
                plt.ylabel("鬱率",fontsize=15)
                plt.xticks(dates[::1],rotation=45)
                plt.tight_layout()

                bio = io.BytesIO()
                plt.savefig(fname=bio, format="png")
                bio.seek(0) 
                img_file = discord.File(fp=bio,filename="graph.png")
                await ctx.channel.send(file=img_file)
                plt.close()

    @commands.command()
    async def utuprofile(self, ctx :discord.ext.commands.Context):

        uuid = str(ctx.message.author.id)

        if ctx.message.reference != None:
            ref_message = await ctx.message.channel.fetch_message(ctx.message.reference.message_id)
            if ref_message.author == self.bot:
                await ctx.send("（あなたがやろうとしていることはわかりますが、ｗ）いや実際ボットのデータもあるからできるんだけど、カスみたいなコード書いたせいで実装が……ｗ")
                return
            uuid = str(ref_message.author.id)
        
        sql_fetch_total_negative = """
            WITH ranked_rates AS (
                SELECT 
                    patient_uuid,
                    SUM(positive_rate * amount) / SUM(amount) AS avg_positive_rate,
                    SUM(negative_rate * amount) / SUM(amount) AS avg_negative_rate,
                    SUM(neutral_rate * amount) / SUM(amount) AS avg_neutral_rate,
                    RANK() OVER (ORDER BY (SUM(negative_rate * amount) / SUM(amount)) DESC) AS rank
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
            WHERE patient_uuid = %s
        """

        sendtxt = "```md\n# 【あなたの総合不幸度順位】\nあなたの今までの発言の不幸度合いは……？```\n"

        with psycopg2.connect(user=self.bot.sqluser, password=self.bot.sqlpassword, host="localhost", port="5432", dbname="depressed_battle") as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(sql_fetch_total_negative, ("1144055461247717506",uuid,))
                row = cur.fetchone()

                member = await ctx.guild.fetch_member(int(uuid))
                membername =  member.name if member.nick == None else member.nick

                if row:
                    rank_degree = self.get_rank(row['avg_negative_rate'],True)
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

            sql_fetch_weekly_rate = """
                SELECT
                    created_at,
                    negative_rate,
                    positive_rate
                FROM depressed
                WHERE patient_uuid = %s AND created_at BETWEEN %s AND %s
                ORDER BY created_at ASC;
            """
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                today = datetime.now().date()
                start_date = today - timedelta(days=7)

                cur.execute(sql_fetch_weekly_rate, (uuid, start_date, today,))
                user_data = cur.fetchall()

                dates = [row["created_at"] for row in user_data]
                negative_rates = [row["negative_rate"] for row in user_data]
                positive_rates = [row["positive_rate"] for row in user_data]

                plt.plot(dates, negative_rates, marker="o", markersize=8, label=f"鬱")
                plt.plot(dates, positive_rates, marker="o", markersize=8, label=f"喜")

                date_format = JapaneseDateFormatter('%m月%d日')
                plt.gca().xaxis.set_major_formatter(date_format)

                member = await ctx.guild.fetch_member(int(uuid))
                # プロット設定
                plt.title(f"{member}の近々一週間の鬱遷移",fontsize=20)
                plt.legend(fontsize=20)
                plt.xlabel("日付",fontsize=15)
                plt.ylabel("鬱率",fontsize=15)
                plt.xticks(dates[::1],rotation=45)
                plt.tight_layout()

                bio = io.BytesIO()
                plt.savefig(fname=bio, format="png")
                bio.seek(0) 
                img_file = discord.File(fp=bio,filename="graph.png")
                await ctx.channel.send(file=img_file)

        plt.close()
        await ctx.channel.send(sendtxt)

    def sqlinsert(self, author_id, positive_rate, negative_rate, neutral_rate):
        today = datetime.now().date()
        author_id = str(author_id)

        with psycopg2.connect(user=self.bot.sqluser, password=self.bot.sqlpassword, host="localhost", port="5432", dbname="depressed_battle") as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT positive_rate, negative_rate, neutral_rate, amount 
                    FROM depressed 
                    WHERE patient_uuid = %s AND created_at = %s
                """, (author_id, today))
                
                result = cur.fetchone()
                
                if result:
                    current_positive, current_negative, current_neutral, current_amount = result
                    new_amount = current_amount + 1

                    new_positive = ((current_positive * current_amount) + positive_rate) / new_amount
                    new_negative = ((current_negative * current_amount) + negative_rate) / new_amount
                    new_neutral = ((current_neutral * current_amount) + neutral_rate) / new_amount

                    cur.execute("""
                        UPDATE depressed 
                        SET positive_rate = %s, negative_rate = %s, neutral_rate = %s, amount = %s
                        WHERE patient_uuid = %s AND created_at = %s
                    """, (new_positive, new_negative, new_neutral, new_amount, author_id, today))
                else:
                    cur.execute("""
                        INSERT INTO depressed (
                            patient_uuid, positive_rate, negative_rate, neutral_rate, created_at, amount
                        ) VALUES (%s, %s, %s, %s, %s, %s)
                    """, (author_id, positive_rate, negative_rate, neutral_rate, today, 1))
                
                conn.commit()

class JapaneseDateFormatter(mdates.DateFormatter):
    def __init__(self, date_format):
        super().__init__(date_format)
        self.japanese_weekdays = ["月", "火", "水", "木", "金", "土", "日"]

    def __call__(self, x, pos=0):
        # xを日付オブジェクトに変換
        date = mdates.num2date(x)
        
        # 日付文字列を取得
        date_str = super().__call__(x, pos)
        
        # 曜日を取得
        weekday_index = date.weekday()  # 0: 月曜日, 6: 日曜日
        weekday_japanese = self.japanese_weekdays[weekday_index]
        
        return f"{date_str}（{weekday_japanese}）"

async def setup(bot):
    await bot.add_cog(DepressedBattle(bot))