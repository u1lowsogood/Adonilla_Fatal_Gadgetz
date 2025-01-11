import discord
from discord.ext import commands
import random
import asyncio

class KUSODEKA(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name="on_message")
    async def kusodekalistener(self,msg : discord.Message):
        if msg.channel.id != 1325770208245317693 or msg.content[:2] == "# ":
            return
        
        if msg.content[:2] == "> " and msg.author.bot:
            return
        
        #async for message in msg.channel.history(limit=1):
        #    latest_message = message
        #    break 
        
        authormsg = f"> from {msg.author.nick or msg.author.name}:"
        contentmsg = f"# {msg.content}"

        await msg.delete()
        await msg.channel.send(f"{authormsg}\n{contentmsg}"[:2000])

async def setup(bot):
    await bot.add_cog(KUSODEKA(bot))


