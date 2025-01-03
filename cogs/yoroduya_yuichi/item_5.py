from textwrap import dedent
import random
import asyncio
import inspect

async def use_item(bot, ctx):

    target = random.randint(0, 9999)
    await ctx.send(dedent(f"""
        {ctx.author.mention} が１万分の１の確率で全財産チャレンジ！
        サイコロで **__ {target} __** の目が出たらチャレンジ成功！
    """))
    await asyncio.sleep(1)
    await ctx.send("# :game_die: ドゥルルルル……")
    await asyncio.sleep(1)
    await ctx.send("# ババン！")
    await asyncio.sleep(1)

    dice = random.randint(0, 9999)
    diff = abs(target - dice)

    player_uuid = str(ctx.author.id)
    u1_balance = bot.economysystem.get_balance(str(216478397570744320))

    conditions = [
        (0, lambda: u1_balance, "__！！！！！！チャレンジ成功全財産略奪！！！！！！__"),
        (1, lambda: u1_balance // 300, "__プラマイ1 超超超ニアミス！！！__"),
        (10, lambda: u1_balance // 700, "__プラマイ10 超ニアミス！！！__"),
        (100, lambda: u1_balance // 2000, "__プラマイ１００！！！__"),
        (500, lambda: combo_bonus(ctx), "__プラマイ５００！ JACKPOT！！__"),
        (1000, lambda: u1_balance // 9000, "__プラマイ１０００ 健闘賞！！！__"),
        (3000, lambda: random.choice([1, 10, 50, 100, 500]), "__プラマイ３０００ 自販機の下の小銭あげますで賞！！！__"),
    ]

    result, amount = await evaluate_conditions(player_uuid, bot, conditions, diff, dice)

    if result is None:
        result = dedent(f"""
            # :game_die: {dice}
            # __チャレンジ失敗！__
        """)
    else:
        result += f"\n# {ctx.author.mention} : {amount} ADP獲得！"

    await ctx.send(result)

async def evaluate_conditions(player_uuid, bot, conditions, diff, dice):
    for threshold, action, message in conditions:
        if diff <= threshold:
            if action:
                result = action()
                if inspect.isawaitable(result):
                    amount = await result
                else:
                    amount = result
                gatya_transfer(player_uuid, bot, amount)
                return dedent(f"""
                    # :game_die: {dice}
                    # {message}
                """), amount
    return None, 0

async def combo_bonus(ctx):
    bonus = 500
    total_bonus = 0
    combo_count = random.randint(3, 13)
    for i in range(combo_count):
        total_bonus += bonus
        await ctx.send(f"{i + 1} COMBO! {ctx.author.mention} +{bonus} ADP")
        await asyncio.sleep(1)
    return total_bonus

def gatya_transfer(player_uuid, bot, amount):
    bot.economysystem.withdraw(str(216478397570744320), amount)
    bot.economysystem.deposit(player_uuid, amount)
