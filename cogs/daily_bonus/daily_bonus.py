import discord.ext
import discord.ext.commands
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
        self.between_hour = 6
        self.base_multiply = 350

    def _connect(self):
        return psycopg2.connect(user=self.bot.sqluser, password=self.bot.sqlpassword, host="localhost", port="5432", dbname="adonilla_economy_system")

    @commands.Cog.listener()
    async def on_command_error(self,ctx, err):
        if isinstance(err, commands.CommandOnCooldown):
            return await ctx.send("コマンド入力早すぎるｗ（2秒に１回制限）")
    
    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 2, type=discord.ext.commands.BucketType.user)
    async def daily(self, ctx):
        user_uuid = str(ctx.author.id) 
        eligible, lasttime = await self.check_and_update_daily_bonus(user_uuid)

        if random.randint(1,30) == 1:
            eligible = True
            await ctx.send("# 強制開催！！！")

        if eligible:
            await self.do(ctx,user_uuid)
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
    
    async def do(self,ctx,user_uuid):

        await ctx.send("# __デイリーADP！__")

        total_money = 0

        result, money = await self.start_daily_bonus_roulette(ctx)
        total_money+=money

        while result % 2 == 0:
            msg = dedent(f"""
            # 偶数が出たのでもう一度！！
            """)
            await ctx.send(msg)
            result, money = await self.start_daily_bonus_roulette(ctx)
            total_money += money

            await asyncio.sleep(1) 

        await asyncio.sleep(1) 
        finished_msg = dedent(f"""
            # __:moneybag:  合計{total_money} ADPを獲得しました！:moneybag:  __
            次回：
            **{self.between_hour} 時間後……**
        """)
        
        await ctx.send(finished_msg)
        self.economysystem.deposit(user_uuid, total_money)

    async def start_daily_bonus_roulette(self, ctx):
        result = self.roll_weighted_dice()

        msg = dedent(f"""
            # :game_die:１～６ ×{self.base_multiply} ADPを獲得できます。
            ` 偶数が出たらもう一度引けるチャンス！？ `
        """)

        await ctx.send(msg)
        await asyncio.sleep(1) 
        await ctx.send(f"# ドゥルルルル……") 
        await asyncio.sleep(1) 

        money = result*self.base_multiply

        finished_msg = dedent(f"""
        {ctx.author.mention}
        # :game_die: {result} x {self.base_multiply} ＝ __ {money} ADP 獲得！__
        """)
        await ctx.send(finished_msg)

        return result, money
    
    def roll_weighted_dice(self):
        dice = [1,2,3,4,5,6]
        result = random.choices(dice,weights=[1,1,1,1,1,1],k=1)[0]
        return result

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
