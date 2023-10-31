from discord.ext import commands
import random
import discord
import json

class MessageRegister(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.PATH = "./cogs/message_register/register_db.json"
        self.registered_dict : dict = None

    def update_db(self):
        with open(self.PATH,"r",encoding="UTF-8") as f:
            self.registered_dict = json.load(f)

    @commands.command(aliases=["rl","レジスタードリスト"])
    async def registeredlist(self, ctx,page:int=1):

        self.update_db()
        keys = list(self.registered_dict.keys())
        msg = "```md\n# 【登録済みキーリストくん】\n/rl [Page] でページ指定ｗ\n\n"
        
        start = (page*20)-20
        end = start+19

        if start >= len(keys):
            await ctx.send("ページデカすぎ クソ田舎")
            return

        for index, key in enumerate(keys[start:end],start=start+1):
            msg += str(index)+". " + key + " - " + self.registered_dict[key][:15].replace("\n","") +"\n"
        else:
            end = index

        msg += "\n<Page."+str(page)+" ["+str(start+1)+"-"+str(end)+"]>"
        msg += "```"

        await ctx.send(msg)

    @commands.command(aliases=["rrm","ランダムレジスターメッセージ"])
    async def randomregistermessage(self,ctx):
        self.update_db()
        picked_key = random.choice(list(self.registered_dict.keys()))
        await ctx.send("```md\n# 「"+picked_key+"」\n```")
        await ctx.send(self.registered_dict[picked_key])

    @commands.command(aliases=["rm","レジスターメッセージ"])
    async def registermessage(self, ctx, key:str = None):

        if ctx.message.reference == None:
            await ctx.send("このコマンドは返信\n # と一緒に\n # 利用してみてねｗ←ｗ")
            return
        if key == None:
            await ctx.send("キーが存在しないねえ＾＾\n【例 /rm おまんこ → 次回以降「おまんこ」に反応】")
            return

        targetmsg : discord.Message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        content = ""

        if targetmsg.attachments == []:
            content = targetmsg.content
        else:
            for attachment in targetmsg.attachments:
                content += attachment.url + "\n"
            content += targetmsg.content

        self.update_db()

        toroku = "上書き" if key in self.registered_dict else "登録"
        
        self.registered_dict[key] = content[:1999]
        
        with open(self.PATH,"w",encoding="UTF-8") as f:
            json.dump(self.registered_dict,f,indent=2,ensure_ascii=False)

        await ctx.send("メッセージを「" + key + "」で"+toroku+"しましたｗ")
        

    @commands.Cog.listener()
    async def on_message(self,msg : discord.Message):

        if msg.author == self.bot.user:
            return
        
        self.update_db()

        if msg.content not in self.registered_dict.keys():
            return
        
        await msg.channel.send(self.registered_dict[msg.content])
        
        


async def setup(bot):
    await bot.add_cog(MessageRegister(bot))