import psycopg2
from psycopg2.extras import DictCursor
from discord.ext import commands
import discord
from datetime import datetime, timedelta
from textwrap import dedent
import asyncio
import random

class DAILY(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.economysystem = self.bot.economysystem
        self.between_hour = 8

    def _connect(self):
        return psycopg2.connect(user=self.bot.sqluser, password=self.bot.sqlpassword, host="localhost", port="5432", dbname="adonilla_economy_system")

    @commands.group(invoke_without_command=True)
    async def daily(self, ctx):
        user_uuid = str(ctx.author.id) 
        eligible, lasttime = await self.check_and_update_daily_bonus(user_uuid)

        if eligible:
            dice = [1,2,3,4,5,6]
            target = random.choices(dice,weights=[1,2,3,3,3,1],k=1)[0]
            multiply = 250
            amount = target*multiply
            msg = dedent(f"""
                # __デイリーADP！__
                # :game_die:１～６ ×{multiply} ADPを獲得できます。
            """)
            await ctx.send(msg)
            await asyncio.sleep(1) 
            await ctx.send(f"# ドゥルルルル……") 
            await asyncio.sleep(1) 
            msg = dedent(f"""
                # {ctx.author.mention}
                # :game_die: {target} x {multiply} ＝ __ {amount} ADP 獲得！__
                次回：{self.between_hour}時間後……
            """)
            await ctx.send(msg)
            self.economysystem.deposit(user_uuid, amount)
        else:
            remaining_time = timedelta(hours=self.between_hour) - (datetime.now() - lasttime)
            hours, remainder = divmod(remaining_time.total_seconds(), 3600)
            minutes = remainder // 60
            msg = dedent(f"""
                {ctx.author.mention}
                まだデイリーボーナスを受け取れません。
                次回：
                **{int(hours)} 時間 {int(minutes)} 分後……**
            """)
            await ctx.send(msg)

    async def check_and_update_daily_bonus(self, uuid):
        now = datetime.now()
        with self._connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("""
                    SELECT lasttime FROM daily_bonus WHERE uuid = %s
                """, (uuid,))
                result = cur.fetchone()

                if result:
                    lasttime = result['lasttime']
                    if now - lasttime < timedelta(hours=self.between_hour):
                        return False, lasttime
                    else:
                        cur.execute("""
                            UPDATE daily_bonus
                            SET lasttime = %s
                            WHERE uuid = %s
                        """, (now, uuid,))
                        conn.commit()
                        return True, now
                else:
                    cur.execute("""
                        INSERT INTO daily_bonus (uuid, lasttime)
                        VALUES (%s, %s)
                    """, (uuid, now,))
                    conn.commit()
                    return True, now

async def setup(bot):
    await bot.add_cog(DAILY(bot))
