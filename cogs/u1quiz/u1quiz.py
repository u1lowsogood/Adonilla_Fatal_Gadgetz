from discord.ext import commands
import discord
import random
from cogs.u1quiz.questions import *
    
class Result():
    def __init__(self):
        self.records = []

    def recordscore(self,question,answer,iscorrect):
        self.records.append((question,answer,iscorrect))

    def getfinalresult(self):
        result = "# 【終了！】\n```md\n# 【RESULT】\n```"
        for answer in self.records:
            result += self.records
            result += answer[0].question
    
    def getmastery(self):
        mastery = [
            "ゆういちプロフェッショナル",
            "ゆういちマニア",
            "ゆういち好き",
            "not ゆういち",
            "冒涜 いちろう",
            "ゆう無知ろう"
            ]
        
class Choice(discord.ui.Button):
    def __init__(self,label,callback,correct=False):
        super().__init__(label=label,style=discord.ButtonStyle.success)
        if correct:
            self.custom_id="correct"
        self.cullbeckk = callback

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("")
        await self.cullbeckk()

        
class ChoicesView(discord.ui.View):
    def __init__(self,callback,question):
        super().__init__(timeout=180)

        for choice in random.sample(question.choices,len(question.choices)):
            #正解の選択肢ならcorrect=Trueにして送信
            self.add_item(Choice(choice,callback,True) if choice == question.choices[0] else Choice(choice,callback))
    

class Quiz():
            
    def __init__(self,ctx,qnum):

        startmsg = [
        "全問正解目指して頑張ろう！",
        "果たして歴代記録は更新されるか！？",
        "歴史を変える挑戦が今始まる！",
        "SHOW TIMEだ！",
        "がんばってね ゆういちより",
        "ゆういちの理解度が試される極限の挑戦ーーーー",
        "頑張れ！頑張れ！頑張れ！頑張れ！頑張れ！"
        ]

        self.header = f"# 【ゆういちクイズ】\nchallanger : {ctx.message.author.mention}\n\n{random.choice(startmsg)}"

        #選択された問題のリスト
        self.questions = QuestionDB().getrandomquestions(6)

        self.ctx = ctx

        #挑戦者
        self.challanger = ctx.message.author 
        #全n問
        self.qnum = qnum
        #現在第n問目
        self.current = 0

        self.msg = None

        self.result = Result()
    
    async def start(self):
        self.msg = await self.ctx.send(content=self.header)
        await self.next()

    async def next(self):

        if self.current > self.qnum:
            return
        
        choicesview = ChoicesView(self.next, self.questions[self.current])

        question_message = f"```md\n# 【第{self.current+1} / {self.qnum}問】\n{self.questions[self.current].question}\n```"
        content = self.header + question_message

        await self.msg.edit(content=content,view=choicesview)

        self.current += 1

class U1quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def u1quiz(self, ctx):

        quiz = Quiz(ctx,6)
        await quiz.start()

async def setup(bot):
    await bot.add_cog(U1quiz(bot))