from discord.ext import commands
import discord
import psycopg2
from psycopg2.extras import DictCursor
import random

class ShowedSenryuRemoveView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)

    @discord.ui.button(label="SHUT UP", style=discord.ButtonStyle.green)
    async def ng(self, interaction : discord.ui.Button, button: discord.Interaction):
        await interaction.message.delete()

class IkkuReadingModal(discord.ui.Modal,title="川柳を詠む"):
    def __init__(self,replyto,bot):
        super().__init__(timeout=None)
        self.replyto: discord.Message = replyto
        self.bot = bot

    senryu = discord.ui.TextInput(
        label='スペース区切りで一句！',
        placeholder="例：「キンタマや 性器こわれる デストロイ」",
        style=discord.TextStyle.short,
        required=True,
        min_length=3,
        max_length=500)

    async def on_submit(self, interaction: discord.Interaction):

        yomite = interaction.user.name if interaction.user.nick==None else interaction.user.nick 

        header = [
            f"{yomite} による美しい一句",
            f"{yomite} による名句",
            f"最高の {yomite} による一句",
            f"{yomite} の世紀の一句",
            f"{yomite} 俳句グランプリ受賞",
            f"川柳マスター{yomite} 晩年の句",
            f"期待のルーキー{yomite} 完璧の一句",
        ]

        apparize = [
            "あっぱれ！",
            "エクセレント！",
            "Beautiful！",
            "アメイジング！",
            "あっぱれ！！",
            "あっぱれろ！",
            "いとおかし"
        ]

        if(len(self.senryu.value)<3):
            return

        content = "```md\n# 【" + random.choice(header) + "】\n```\n"
        for bunsetu in self.senryu.value.split():
            content += f"> **{bunsetu}**\n"
        content += f"# 【{random.choice(apparize)}】"

        self.sqlinsert(self.senryu.value)

        await interaction.response.defer()
        evaluation = await self.replyto.reply(content)
        await evaluation.add_reaction("👍")

    def sqlinsert(self,senryu):
        sql = """
            insert into deathsenryu(
                author_uid
                ,senryu
            )values(
                %s
                ,%s
            )
        """
    
        try:
            with psycopg2.connect(user=self.bot.sqluser, password=self.bot.sqlpassword,host="localhost", port="5432", dbname="deathsenryu") as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, (self.replyto.author.id, senryu))
                    #print(f"sql inserted: {senryu}")
        except:
            print("something happen w")

class KokodeIkkuView(discord.ui.View):

    def __init__(self,replyto,bot):
        super().__init__(timeout=300)
        self.replyto = replyto
        self.bot = bot
    
    @discord.ui.button(label="詠む！", style=discord.ButtonStyle.green)
    async def ok(self, interaction : discord.ui.Button, button: discord.Interaction):
        if interaction.user.id != self.replyto.author.id:
            await interaction.response.send_message("他人の川柳を勝手に詠めないよ\n/deathsenryu コマンドで一句読めるよ")
            return
        inputmodal = IkkuReadingModal(self.replyto,self.bot)
        await interaction.response.send_modal(inputmodal)
        await interaction.message.delete()

    @discord.ui.button(label="またこんど", style=discord.ButtonStyle.gray)
    async def ng(self, interaction : discord.ui.Button, button: discord.Interaction):
        if interaction.user.id != self.replyto.author.id:
            await interaction.response.send_message("他人の川柳を勝手に消すな！ｗ")
            return
        await interaction.message.delete()
        
class DeathSenryu(commands.Cog):
            
    def __init__(self, bot):
        self.show_permille = 5*10
        self.read_permille = 5*10
        self.bot = bot

    @commands.command()
    async def cimerasenryu(self, ctx, amount :int = 3):
        if amount < 1:
            await ctx.send("数字が小さすぎる")
            return
        elif amount > 11:
            await ctx.send("数字が大きすぎる（１０以下で……ｗ）")
            return
        
        with psycopg2.connect(user=self.bot.sqluser, password=self.bot.sqlpassword,host="localhost", port="5432", dbname="deathsenryu") as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(f"SELECT * FROM deathsenryu ORDER BY random() limit {amount}")
                rows = cur.fetchall()

                bunsetus = []

                for row in rows:
                    splited_senryu = row["senryu"].split()
                    bunsetus.append(random.choice(splited_senryu))

                content = f"```md\n#【デスキメラ川柳】\n```\n"

                for bunsetu in bunsetus:
                    content += f"> **{bunsetu}**\n"
                await ctx.message.reply(content)

    @commands.command()
    async def deathsenryu(self, ctx):
        await self.kokodeikku(ctx.message)

    @commands.command()
    async def randomsenryu(self, ctx):
        await self.showrandomsenryu(ctx.message)

    #REMAIN: listsenryu,cimerasenryu        
    
    @commands.Cog.listener(name="on_message")
    async def senryu_verdict(self,msg : discord.Message):
        if msg.author == self.bot.user or msg.author.bot or "/" in msg.content:
            return
        if random.randint(0,999) < self.show_permille:
            await self.showrandomsenryu(msg)
            return
        if random.randint(0,999) < self.read_permille:
            await self.kokodeikku(msg)
            return


    async def kokodeikku(self,msg : discord.Message):
        askikkumsgs = [
            "ここで一句！",
            "ここで一句！！！",
            "ここで一句ｗ",
            "今の気持ちは？",
            "今の気持ちは？ｗ",
            "ここで一言！",
            "川柳を 読んでみようよ レッツゴー",
            "是非今の気分を一句お願いします!",
            "川柳グランプリ開催！"
        ]

        view = KokodeIkkuView(msg,self.bot)
        await msg.reply(content=random.choice(askikkumsgs), view=view)

    async def showrandomsenryu(self,msg : discord.Message):
        
        iku = [
            "今の貴方にこそ贈る 美しい一句",
            "そんなあなたにピッタリの川柳",
            "あなたにピッタリ！最高の一句",
            "貴方の今の発言、要約するとこのようになります。",
            "それってつまり、こういうこと？",
            "その発言に合致する川柳があります！",
            "あーわかる。こういうことだよね",
            "そんな貴方の気持ちに寄り添う、静かな一句",
        ]

        #try:
        with psycopg2.connect(user=self.bot.sqluser, password=self.bot.sqlpassword,host="localhost", port="5432", dbname="deathsenryu") as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("SELECT * FROM deathsenryu ORDER BY random() limit 1")
                row = cur.fetchone()
                senryu = row["senryu"]

                member = await msg.guild.fetch_member(row["author_uid"])
                yomibito =  member.name if member.nick == None else member.nick

                content = f"```md\n#【{random.choice(iku)}】\n```\n"

                for bunsetu in senryu.split():
                    content += f"> **{bunsetu}**\n"
                content += f"\n*――――by {yomibito}*"
                await msg.reply(content,view=ShowedSenryuRemoveView())
        #except:
        #    print("今はSQLサーバーが動いてないっぽいンゴねぇｗ")


async def setup(bot):
    await bot.add_cog(DeathSenryu(bot))