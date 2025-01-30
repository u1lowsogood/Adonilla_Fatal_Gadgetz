import discord
import discord.ext
import discord.ext.commands
from discord.ext import commands

from cogs.exp.expsystem import ExpSystem


class EXP_Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.expsystem : ExpSystem = self.bot.system.expsystem

    async def show_gauge(self,ctx):
        status = self.expsystem.get_status(ctx.author.id)

        level = status['level']
        bunshi = status['exp_current']
        bunbo  = status['exp_max']

        gauge_length = 20
        progress = round((bunshi / bunbo) * gauge_length)

        gauge = "|" + "-" * (progress - 1) + "🤓" + "-" * (gauge_length - progress) + "|"

        sendmsg = f"# Level. {level}\n"
        sendmsg += f"{gauge} ({bunshi}/{bunbo})\n\n"

        await ctx.send(sendmsg)

    @commands.group(invoke_without_command=True,aliases=["lv"])
    async def level(self, ctx):
        await self.show_gauge(ctx)

    @level.command()
    async def add(self, ctx : discord.ext.commands.Context , amount : int):
        await self.expsystem.add_exp(ctx.author, amount)
        await self.show_gauge(ctx)

    @level.command()
    async def ranking(self, ctx : discord.ext.commands.Context):
        ranking = self.expsystem.get_ranking(10)
        ranking_msg = "```md\n# 【アドンイラ経験値番付】\n\n"

        for order, (user_uuid, balance, exp, max) in enumerate(ranking):
            member = ctx.guild.get_member(user_uuid)
            if not member:
                continue
            user_name = member.nick or member.name
            ranking_msg += f"{order+1}. {user_name}\n> Lv. {balance} ({exp}/{max})\n"

        ranking_msg += "```"
        await ctx.send(ranking_msg)

async def setup(bot):
    await bot.add_cog(EXP_Commands(bot))