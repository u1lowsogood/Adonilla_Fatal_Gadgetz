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
    result = ""

    amount = bot.economysystem.get_balance(str(216478397570744320))

    if abs(target-dice)==0:
        gatya_transfer(ctx,bot,amount)

        result = dedent(f"""
            # :game_die: {dice}
            # __！！！！！！チャレンジ成功！！！！！！__
        """)
    elif abs(target-dice)<1:
        amount //= 300
        gatya_transfer(ctx,bot,amount)

        result = dedent(f"""
            # :game_die: {dice}
            # __プラマイ1 超超超ニアミス！！！__
        """)
    elif abs(target-dice)<10:
        amount //= 700
        gatya_transfer(ctx,bot,amount)

        result = dedent(f"""
            # :game_die: {dice}
            # __プラマイ10 超ニアミス！！！__
        """)
    elif abs(target-dice)<100:
        amount //= 4000
        gatya_transfer(ctx,bot,amount)

        result = dedent(f"""
            # :game_die: {dice}
            # __プラマイ１００！！！__
        """)
    elif abs(target-dice)<1000:
        amount //= 9000
        gatya_transfer(ctx,bot,amount)

        result = dedent(f"""
            # :game_die: {dice}
            # __プラマイ１０００ 健闘賞！！！__
        """)
    elif abs(target-dice)<3000:
        a = [1,10,50,100,500]
        amount = random.choice(a)
        gatya_transfer(ctx, bot, amount)

        result = dedent(f"""
            # :game_die: {dice}
            # __プラマイ３０００ 自販機の下の小銭あげますで賞！！！__
        """)
    else:
        result = dedent(f"""
            # :game_die: {dice}
            # __チャレンジ失敗！__
        """)
        await ctx.send(result)
        return

    result += f"# {ctx.author.mention} : {amount} ADP獲得！"
    await ctx.send(result)

def gatya_transfer(ctx, bot,amount):
    bot.economysystem.withdraw(str(216478397570744320), amount)
    bot.economysystem.deposit(str(ctx.author.id), amount)