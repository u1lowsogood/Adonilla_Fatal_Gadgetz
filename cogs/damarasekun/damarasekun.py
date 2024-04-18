import discord
from discord.ext import commands
import random
import asyncio

class Damarasekun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.n = 0

    @commands.command(aliases=["黙らせ君","projectwinter","winter"])
    async def damarasekun(self, ctx, *without):
        member : discord.Member = ctx.message.author
        if member.voice == None:
            await ctx.channel.send("VC内で使ってねえ")
            return
        
        players = member.voice.channel.members

        spectators = [await commands.converter.MemberConverter().convert(ctx, member) for member in without]
        players = filter(lambda player : player not in spectators, players)

        spec_str = ""
        if len(spectators) > 0:
            spec_str += "```md\n# 【観戦者】\n"+"\n".join([str(i+1)+". "+spec.display_name for i, spec in enumerate(spectators)])+"```"
        
        if self.n % 2 == 0:
            await ctx.channel.send("スピーカーミュート開始！"+spec_str)
            for player in players:
                if player.voice.deaf == False:
                    await player.edit(deafen=True)
        else:
            await ctx.channel.send("スピーカーミュート解除！")
            for player in players:
                if player.voice.deaf == True:
                    await player.edit(deafen=False)
        self.n += 1

async def setup(bot):
    await bot.add_cog(Damarasekun(bot))