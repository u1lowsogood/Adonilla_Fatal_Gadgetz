import discord
import discord.ext
import discord.ext.commands
from discord.ext import commands

from cogs.exp.expsystem import ExpSystem


class EXP_Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.expsystem : ExpSystem = self.bot.system.expsystem

    @commands.group(invoke_without_command=True,aliases=["lv"])
    async def level(self, ctx):
        await self.expsystem.show_gauge(ctx)

    @level.command()
    async def add(self, ctx : discord.ext.commands.Context, mention : discord.Member, amount : int):
        await self.expsystem.add_exp(mention, amount)
        await self.expsystem.show_gauge(ctx, mention)

    @level.command()
    async def ranking(self, ctx : discord.ext.commands.Context):
        ranking = self.expsystem.get_ranking(10)
        ranking_msg = "```md\n# 【アドンイラ経験値番付】\n\n"

        for order, (user_uuid, balance, exp, mx) in enumerate(ranking):
            member = ctx.guild.get_member(user_uuid)
            if not member:
                continue
            user_name = member.nick or member.name
            ranking_msg += f"{order+1}. {user_name}\n> Lv. {balance} ({exp}/{mx})\n"

        ranking_msg += "```"
        await ctx.send(ranking_msg)

async def setup(bot):
    await bot.add_cog(EXP_Commands(bot))