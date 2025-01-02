from textwrap import dedent
import random
import asyncio

async def use_item(bot, ctx):
    target = random.randint(0,9999)
    msg = dedent(f"""
        {ctx.author.mention} が１万分の１の確率で全財産チャレンジ！
        サイコロで **__ {target} __**の目が出たらチャレンジ成功！
    """)
    await ctx.send(msg)
    await asyncio.sleep(1) 
    await ctx.send(f"# :game_die: ドゥルルルル……") 
    await asyncio.sleep(1) 
    await ctx.send(f"# ババン！")    
    await asyncio.sleep(1) 
    
    dice = random.randint(0,9999)
    result = dedent(f"""
            # :game_die: {dice}
            # __チャレンジ失敗！__
    """)

    if target == dice:
        amount = bot.economysystem.get_balance(str(216478397570744320))
        bot.economysystem.withdraw(str(216478397570744320), amount)
        bot.economysystem.deposit(str(ctx.author.id), amount)

        result = dedent(f"""
            # :game_die: {dice}
            # __チャレンジ成功！！！__
            # {amount} ADP獲得！
        """)

    await ctx.send(result)