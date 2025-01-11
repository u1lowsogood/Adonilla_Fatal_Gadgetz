from discord.ext import commands
import psycopg2
from psycopg2.extras import DictCursor
from textwrap import dedent

from cogs.shops.yoroduya_yuichi.funcs import item_1, item_2, item_3,item_4

class YORODUYA_U1(commands.Cog):
    def __init__(self, bot):
        self.shop_id = 1
        self.bot = bot
        self.economysystem = self.bot.economysystem
        self.shopsystem = self.bot.shopsystem
        self.user_status = {}

        self.ITEM_HANDLERS = [
            item_1.use_item,
            item_2.use_item,
            item_3.use_item,
            item_4.use_item,
        ]

        self.usage = dedent("""
            ```md
            # 【用法】
            購入方法：
            /u1shop buy アイテム番号
            使用方法：
            /u1shop use アイテム番号
            インベントリ：
            /u1shop inventory
            ```
        """)

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
        for item in items:
            msg += dedent(f"""
                {item[0]}. 『{item[1]}』
                {item[2]}
                > {item[3]} ADP
            """)
        msg += "```"
        msg += self.usage

        await ctx.send(msg)

    @u1shop.command()
    async def buy(self, ctx, item_id : int, amount: int = 1):
        try:
            msg = self.shopsystem.purchase(str(ctx.author.id), self.shop_id, item_id, amount)
            await ctx.send(msg)

        except ValueError as e:
            await ctx.send(f"{e}")

    @u1shop.command()
    async def use(self, ctx, item_id : int):
        if self.shopsystem.consume_item(str(ctx.author.id), self.shop_id, item_id):
        
            if self.user_status.get(ctx.author.id, False):
                return

            self.user_status[ctx.author.id] = True
            await self.item_use(item_id, ctx)

            self.user_status[ctx.author.id] = False

        else:
            await ctx.send("そのアイテム持ってないよ笑")

    async def item_use(self, used_item, ctx):
        await self.ITEM_HANDLERS[used_item-1](self.bot, ctx)

    @u1shop.command()
    async def inventory(self, ctx):
        items = self.shopsystem.get_inventory_items(str(ctx.author.id), self.shop_id)
        sendmsg = dedent(f"""
            ```md
            # 【インベントリ：よろづやゆういち】
            あなたはバッグを開いた。
            ``````md
        """)
        if len(items)==0:
            sendmsg+="空"
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
