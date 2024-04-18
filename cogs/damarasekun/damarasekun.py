import discord
from discord.ext import commands
import random
import asyncio

class Damarasekun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.n = 0

    @commands.command(aliases=["黙らせ君","projectwinter","winter"])
    async def damarasekun(self, ctx):
        member : discord.Member = ctx.message.author
        if member.voice == None:
            await ctx.channel.send("VC内で使ってねえ")
            return
        
        connected: discord.VoiceChannel = member.voice.channel
        
        if self.n % 2 == 0:
            await ctx.channel.send("スピーカーミュート開始！")
            for member in connected.members:
                if member.voice.deaf == False:
                    await member.edit(deafen=True)
        else:
            await ctx.channel.send("スピーカーミュート解除！")
            for member in connected.members:
                if member.voice.deaf == True:
                    await member.edit(deafen=False)

        self.n += 1

async def setup(bot):
    await bot.add_cog(Damarasekun(bot))