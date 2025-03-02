from fancy_text import fancy
from discord.ext import commands
import discord
import random

class TextCooler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.count = 0
        self.how = [
            fancy.bold,
        ]

    @commands.command(aliases=["tc"])
    async def textcooler(self, ctx : commands.Context, txt_orig : str = None):

        if ctx.message.reference != None:
            msg_orig : discord.Message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            txt_orig = msg_orig.content

        if txt_orig == None:
            await ctx.send("返信 or 引数に指定し（なさい）\n 例： /textcooler hello")
            return
        
        txt_decorated = self.how[self.count % len(self.how)](txt_orig)
        self.count+=1
        
        await ctx.reply(txt_decorated)

async def setup(bot):
    await bot.add_cog(TextCooler(bot))