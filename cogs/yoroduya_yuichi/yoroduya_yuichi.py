from discord.ext import commands
import psycopg2
from psycopg2.extras import DictCursor
from textwrap import dedent

from cogs.yoroduya_yuichi import item_1

class YORODUYA_U1(commands.Cog):
    def __init__(self, bot):
        self.shop_id = 1
        self.bot = bot
        self.economysystem = self.bot.economysystem
        self.shopsystem = self.bot.shopsystem

        self.ITEM_HANDLERS = {
            1: item_1.use_item,
        }

        self.usage = dedent("""
            ```md
            # 【用法】
            商品一覧：
            /u1shop
            購入方法：
            /u1shop buy 商品番号
            購入した物品一覧を確認：
            /u1shop inventory
            使用方法：
            /u1shop use アイテム番号
            ```
        """)

    def _connect(self):
        return psycopg2.connect(
            user=self.bot.sqluser,
            password=self.bot.sqlpassword,
            host="localhost",
            port="5432",
            dbname="yoroduya_u1"
        )

    @commands.group(invoke_without_command=True)
    async def u1shop(self, ctx):
        msg = ""
        welcome = dedent(f"""
            ```md
            # 【よろづやゆういち】

            チリンチリン…… 
            『{ctx.author.nick or ctx.author.name}』さん、いらっしゃい！品揃え抜群だよ！
            ```
        """)
        msg += welcome
        msg += "```md\n"

        items = self.shopsystem.get_shop_items(self.shop_id)
        for i, item in enumerate(items, start=1):
            msg += dedent(f"""
                {i}. 『{item[0]}』
                {item[1]}
                > {item[2]} ADP
            """)
        msg += "```"
        msg += self.usage

        await ctx.send(msg)

    @u1shop.command()
    async def buy(self, ctx, item_id : int, amount: int = 1):
        try:
            msg = self.shopsystem.purchase(str(ctx.author.id), item_id, amount)
            await ctx.send(msg)
        except ValueError as e:
            await ctx.send(f"エラー: {e}")

    @u1shop.command()
    async def use(self, ctx, item_id : int):
        try:
            used_item = self.shopsystem.consume_item(str(ctx.author.id), item_id)
            await self.item_use(used_item, ctx)
        except ValueError as e:
            await ctx.send(f"エラー: {e}")

    async def item_use(self, used_item, ctx):
        await self.ITEM_HANDLERS[used_item](self.bot, ctx)

    @u1shop.command()
    async def inventory(self, ctx):
        items = self.shopsystem.get_inventory_items(str(ctx.author.id), self.shop_id)
        sendmsg = dedent(f"""
            ```md
            # 【インベントリ：よろづやゆういち】
            あなたはバッグを開いた。
            ``````md
        """)
        for item in items:
            sendmsg += f"{item[0]}. 『{item[1]}』 x{item[3]}\n{item[2]}\n"
        sendmsg += dedent("""
            ``````
            使用方法：
            /u1shop use アイテム番号
            ```
        """)
        await ctx.send(sendmsg)
        
async def setup(bot):
    await bot.add_cog(YORODUYA_U1(bot))
