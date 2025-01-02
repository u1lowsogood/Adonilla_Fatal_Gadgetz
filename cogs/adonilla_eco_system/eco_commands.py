from discord.ext import commands
import discord

class ECOMMANDS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.economysystem = self.bot.economysystem

    @commands.group(invoke_without_command=True,aliases=["aeco"])
    async def adonnilaecosystem(self, ctx):
        help = """
```md
# 【Adonnila Eco System 解説】
/aeco
コマンド一覧
/aeco balance
残高確認
/aeco transfer 送金相手へのメンション 値段
送金
/aeco ranking
長者番付
/shops
アドンイラエコシステムで使用可能なコンテンツ一覧を表示します。
```
"""
        await ctx.send(help)

    @adonnilaecosystem.command(aliases=["zandaka"])
    async def balance(self, ctx, mention :discord.User = None):
        user = ctx.author if mention==None else mention
        balance = self.economysystem.get_balance(str(user.id))

        balance_msg = f"""
{user.mention} の現在の残高は……
## :moneybag: **__{balance} ADP__** です！
"""
        await ctx.send(balance_msg)

    @adonnilaecosystem.command(aliases=["soukin"])
    async def transfer(self, ctx, mention :discord.User, amount: int, mention_from :discord.User = None):

        member_from = ctx.author
        if mention_from != None:
            if ctx.author.id == 216478397570744320:
                member_from = mention_from
            else:
                await ctx.send(f"他人の口座から送金する機能は管理人限定です。")
                return

        balance = self.economysystem.get_balance(str(member_from.id))
        if balance < amount:
            await ctx.send(f"残高が不足しています！\n不足額: {amount - balance} ADP")
            return
        
        try:
            self.economysystem.withdraw(str(member_from.id), amount)
            self.economysystem.deposit(str(mention.id), amount)
            await ctx.send(f"{member_from.mention} が {mention.mention} に {amount} ADP 送金しました。")
        except ValueError as e:
            await ctx.send(f"エラー: {e}")

    @adonnilaecosystem.command()
    async def give(self, ctx, mention :discord.User, amount: int):
        if ctx.author.id != 216478397570744320:
            return
        self.economysystem.deposit(str(mention.id), amount)
        await ctx.send(f"{mention.mention} に {amount} ADP付与しました！")

    @adonnilaecosystem.command(aliases=["bosshu"])
    async def forfeiture(self, ctx, mention :discord.User, amount: int):
        if ctx.author.id != 216478397570744320:
            return
        self.economysystem.withdraw(str(mention.id), amount)
        await ctx.send(f"{mention.mention} から {amount} ADP没収しました！")

    @adonnilaecosystem.command(aliases=["banduke","banzuke"])
    async def ranking(self, ctx):
        ranking = self.economysystem.get_ranking()
        ranking_msg = "```md\n# 【アドンイラ長者番付】\n\n"

        for order, (user_uuid, balance) in enumerate(ranking, start=1):
            member = ctx.guild.get_member(int(user_uuid))
            user_name = member.nick or member.name
            ranking_msg += f"{order}. {user_name}\n{balance} ADP\n\n"

        ranking_msg += "```"
        await ctx.send(ranking_msg)


async def setup(bot):
    await bot.add_cog(ECOMMANDS(bot))
