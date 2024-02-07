from discord.ext import commands
import discord
import random
from cogs.u1quiz.questions import *

class AnswerRecord():
    def __init__(self,question,answer,iscorreft):
        self.question = question
        self.answer = answer
        self.iscorrect = iscorreft
    
class Score():
    def __init__(self):
        self.records = []

    def addanswerrecord(self,answerrecord):
        self.records.append(answerrecord)

    def getfinalresultmsg(self):
        score = 0
        result = "# 【終了！】\n```md\n# 【RESULT】\n```\n"
        for i, record in enumerate(self.records):
            score = score+1 if record.iscorrect else score
            result += ":white_check_mark: **正解！**\n" if record.iscorrect else ":x:  **不正解……**\n"
            result += f"```md\n{i+1}. {record.question.question} → あなたの回答「{record.answer}」\n```\n"
            result += f"> {record.question.reason}\n\n"
        result += f"# あなたのスコア： {score} / {len(self.records)}\n# 称号は「{self.getmastery(score)}」です！"
        return result
    
    def getmastery(self,score):
        mastery = [
            "ゆういちプロフェッショナル",
            "ゆういちマニア",
            "ゆういち好き",
            "not ゆういち",
            "冒涜 いちろう",
            "ゆう無知ろう"
            ]
        return mastery[len(mastery) - score]

class Choice(discord.ui.Button):
    def __init__(self,label,currentquestion,nextquestion,score,correct=False):
        super().__init__(label=label,style=discord.ButtonStyle.success)
        if correct:
            self.custom_id="correct"
        self.currentquestion = currentquestion
        self.score = score
        self.nextquestion = nextquestion

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        #await interaction.response.send_message(content="：｝",delete_after=1)
        self.score.addanswerrecord(AnswerRecord(self.currentquestion,self.label, self.custom_id=="correct"))
        await self.nextquestion()

        
class ChoicesView(discord.ui.View):
    def __init__(self,callback,question,score):
        super().__init__(timeout=180)

        for choice in random.sample(question.choices,len(question.choices)):
            #正解の選択肢ならcorrect=Trueにして送信
            self.add_item(Choice(choice,question,callback,score,True) if choice == question.choices[0] else Choice(choice,question,callback,score))
    

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

        self.score = Score()
    
    async def start(self):
        self.msg = await self.ctx.send(content=self.header)
        await self.next()

    async def next(self):
                
        if self.current >= self.qnum:
            await self.finish()
            return
        
        currentquestion = self.questions[self.current]

        choicesview = ChoicesView(self.next, currentquestion, self.score)

        question_message = f"```md\n# 【第 {self.current+1} / {self.qnum} 問】\n{currentquestion.question}\n```"

        content = self.header + question_message

        await self.msg.edit(content=content,view=choicesview)

        self.current += 1

    async def finish(self):
        await self.ctx.send(self.score.getfinalresultmsg())


class U1quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def u1quiz(self, ctx):

        quiz = Quiz(ctx,6)
        await quiz.start()

async def setup(bot):
    await bot.add_cog(U1quiz(bot))