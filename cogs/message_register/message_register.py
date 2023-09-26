from discord.ext import commands
import random
import discord
import json

class MessageRegister(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.PATH = ".cogs/message_register/register_db.json"
        self.register_dict : dict = None

    def update_db(self):
        with open(self.PATH) as f:
            self.register_dict = json.load(f)

    @commands.command(aliases=["rl","レジストリスト"])
    async def registlist(self, ctx):
        self.update_db()
        msg = "```md\n# 【登録済み単語リストくん】\n\n"
        for index, key in enumerate(self.register_dict.keys):
            msg += str(index)+"." + key + "\n"
        msg += "```"
        ctx.send(msg)

    @commands.command(aliases=["rm","レジストメッセージ"])
    async def registmessage(self, ctx, key:str = None):

        if key == None:
            await ctx.send("キーが存在しないねえ＾＾\n【例 /rm おまんこ → 次回以降「おまんこ」に反応】")
            return
        if ctx.message.reference == None:
            await ctx.send("このコマンドは返信\n # と一緒に\n # 利用してみてねｗ←ｗ")
            return
        
        self.update_db()

        if ctx.message.attachments == []:
            self.register_dict[key] = ctx.message.content
        else:
            content = ""
            for i in len(ctx.message.attachments):
                content += ctx.message.attachments[i].url + "\n"
            content += ctx.message.content
            self.register_dict[key] = content[:2000]

        with open(self.PATH) as f:
            json.dump(self.register_dict,f,indent=2)

    @commands.Cog.listener()
    async def on_message(self,msg : discord.Message):

        if msg.author == self.bot.user:
            return
        
        self.update_db()

        if msg.content not in self.register_dict.keys:
            return
        
        msg.channel.send(self.register_dict[msg.content])
        
        


async def setup(bot):
    await bot.add_cog(MessageRegister(bot))