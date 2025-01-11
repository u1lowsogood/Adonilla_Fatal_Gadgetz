from discord.ext import commands
import psycopg2
from psycopg2.extras import DictCursor
from textwrap import dedent

from cogs.shops.premium_shop import purchase_premium

class PREMIUM(commands.Cog):
    def __init__(self, bot):
        self.shop_id = 2
        self.bot = bot
        self.economysystem = self.bot.economysystem
        self.shopsystem = self.bot.shopsystem
        self.premiumsystem = self.bot.premiumsystem

        self.usage = dedent("""
            ```md
            # 【用法】
            購入方法：
            /pshop buy アイテム番号
            使用方法：
            /pshop use アイテム番号
            インベントリ：
            /pshop inventory
            ```
        """)

    def _connect(self):
        return psycopg2.connect(
            user=self.bot.sqluser,
            password=self.bot.sqlpassword,
            host="localhost",
            port="5432",
            dbname="adonilla_economy_system"
        )

    @commands.group(invoke_without_command=True)
    async def pshop(self, ctx):
        msg = ""
        welcome = dedent(f"""
            ```md
            # 【プレミアムショップ】

            都内アドンイラタワービル最上階、秘密のペントハウス……
            ようこそ、『{ctx.author.nick or ctx.author.name}』様。当店はプレミアムな品を揃えております。
            ```
        """)
        msg += welcome
        msg += "```md\n"

        items = self.shopsystem.get_shop_items(self.shop_id)
        for item in items:
            msg += dedent(f"""
                {item[0]}. 『{item[1]}』
                {item[2]}
                > {item[3]} ADP
            """)
        msg += "```"
        msg += self.usage

        await ctx.send(msg)

    @pshop.command()
    async def buy(self, ctx, item_id : int, amount: int = 1):
        try:
            msg = self.shopsystem.purchase(str(ctx.author.id), item_id, amount)
            await ctx.send(msg)
        except ValueError as e:
            await ctx.send(f"{e}")

    @pshop.command()
    async def use(self, ctx, item_id : int):
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT premium_level FROM premium_shop WHERE item_id = %s
                """, (item_id,))

                purchased_premium_level = int(cur.fetchone()[0])-1
                role_id = self.premiumsystem.ROLES[purchased_premium_level]

                if ctx.author.get_role(role_id[1]) == None:
                    if self.shopsystem.consume_item(str(ctx.author.id), item_id):
                        await purchase_premium.use_item(self.bot,ctx,role_id)
                    else:
                        await ctx.send("引換券持ってないよ笑")
                else:
                    await ctx.send(f"既にロール <@&{role_id[0]}> を保有しています！")
                    return
                
    @pshop.command()
    async def checkmy(self, ctx):
        await ctx.send(self.premiumsystem.get_level_sum(ctx.author))

    @pshop.command()
    async def inventory(self, ctx):
        items = self.shopsystem.get_inventory_items(str(ctx.author.id), self.shop_id)
        sendmsg = dedent(f"""
            ```md
            # 【インベントリ：プレミアムショップ】
            あなたは財布（高級な皮の！）を開いた。
            ``````md
        """)
        if len(items)==0:
            sendmsg+="空"
        for item in items:
            sendmsg += f"{item[0]}. 『{item[1]}』 x{item[3]}\n{item[2]}\n"
        sendmsg += dedent("""
            ``````
            使用方法：
            /pshop use アイテム番号
            ```
        """)
        await ctx.send(sendmsg)

async def setup(bot):
    await bot.add_cog(PREMIUM(bot))
