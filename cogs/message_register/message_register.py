from discord.ext import commands
import random
import discord
import json

class MessageRegister(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.PATH = "./register_db.json"
        self.register_dict : dict = None

    def update_db(self):
        with open(self.PATH) as f:
            self.register_dict = json.load(f)

    @commands.command(aliases=["rm","レジストメッセージ"])
    async def registmessage(self, ctx, key:str = None):

        if key == None:
            await ctx.send("キーを指定してねｗ")
            return
        if ctx.message.reference == None:
            await ctx.send("このコマンドは返信\n # と一緒に\n # 利用してみてねｗ←ｗ")
            return
        
        self.update_db()
        self.register_dict[key] = ctx.message

    @commands.Cog.listener()
    async def on_message(self,msg : discord.Message):
        self.update_db()

        if msg.content not in self.register_dict.keys:
            return
        


async def setup(bot):
    await bot.add_cog(MessageRegister(bot))