import psycopg2
from psycopg2.extras import DictCursor
from discord.ext import commands
import discord

class SHOPS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.economysystem = self.bot.economysystem

    def _connect(self):
        return psycopg2.connect(user=self.bot.sqluser, password=self.bot.sqlpassword, host="localhost", port="5432", dbname="adonilla_economy_system")

    @commands.group(invoke_without_command=True)
    async def shops(self, ctx):
            shop_list = """
```md
# 【Adonnila SHOPS】
アドンイラエコシステムで使用可能なコンテンツ一覧を表示するよ。
```
"""
            for shop in self.get_shops():
                shop_list += f"""```md
# 【{shop[1]}】

{shop[2]}
```"""
            await ctx.send(shop_list)

    def get_shops(self):
        with self._connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("SELECT id,name,description FROM shops ORDER BY id DESC")
                result = cur.fetchall()
                shop_list = [(row['id'], row['name'], row['description']) for row in result]
                return shop_list

async def setup(bot):
    await bot.add_cog(SHOPS(bot))
