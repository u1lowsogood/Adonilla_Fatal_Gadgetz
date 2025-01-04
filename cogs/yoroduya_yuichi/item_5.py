from textwrap import dedent
import random
import asyncio
import inspect

async def use_item(bot, ctx):

    target = random.randint(0, 9999)
    await ctx.reply(dedent(f"""
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
        (1, lambda: u1_balance // 50, "__プラマイ1 超超超ニアミス:moneybag: ！！！__"),
        (10, lambda: u1_balance // 300, "__:moneybag: プラマイ10 超ニアミス:moneybag: ！！！__"),
        (100, lambda: u1_balance // 1000, "__:moneybag: プラマイ１００！！！:moneybag: __"),
        (500, lambda: combo_bonus(ctx), "__:moneybag: ジャックポット終了:moneybag: ！__"),
        (1000, lambda: u1_balance // 9000, "__:moneybag:プラマイ１０００ 健闘賞！！！:moneybag:__"),
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

    await ctx.reply(result)

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
    bonus_steps = [
        (3, 100, ["", ""]),
        (6, 300, ["**", "**"]),
        (9, 600, ["__**", "**__"]),
        (12, 1200, ["## __", "__"]),
        (15, 5000, ["# __*MAX COMBO！！！", "*__"]),
    ]
    bonus_iterator = iter(bonus_steps)
    current_range, current_bonus, decorator = next(bonus_iterator)

    total_bonus = 0
    combo_count = random.randint(4, 13)

    await ctx.reply("# !!:moneybag: プラマイ５００JACKPOT :moneybag: スタート!!\nhttps://media1.tenor.com/m/0YSqS0ixtm4AAAAd/pon.gif")

    for i in range(combo_count):
        if i + 1 > current_range:
            current_range, current_bonus, decorator = next(bonus_iterator)

        combomsg = f"{decorator[0]}{ctx.author.mention} {i + 1} COMBO! :moneybag:+{current_bonus} ADP{decorator[1]}"
        await ctx.send(combomsg)
        await asyncio.sleep(1)
        total_bonus += current_bonus

    return total_bonus

def gatya_transfer(player_uuid, bot, amount):
    bot.economysystem.withdraw(str(216478397570744320), amount)
    bot.economysystem.deposit(player_uuid, amount)
