from textwrap import dedent
import random
import asyncio
import inspect
import cogs.yoroduya_yuichi.combo as combo

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
    kokko_uuid = bot.economysystem.get_kokko_uuid()
    kokko_balance = bot.economysystem.get_balance(kokko_uuid)

    conditions = [
        (0, lambda: kokko_balance, "__！！！！！！チャレンジ成功全財産略奪！！！！！！__"),
        (1, lambda: kokko_balance // 50, "__プラマイ1 超超超ニアミス:moneybag: ！！！__"),
        (10, lambda: kokko_balance // 300, "__:moneybag: プラマイ10 超ニアミス:moneybag: ！！！__"),
        (100, lambda: infinite_combo_bonus(ctx), "__:moneybag: 無限ジャックポット終了！！！:moneybag: __"),
        (500, lambda: combo_bonus(ctx), "__:moneybag: ジャックポット終了:moneybag: ！__"),
        (1000, lambda: kokko_balance // 9000, "__:moneybag:プラマイ１０００ 健闘賞！！！:moneybag:__"),
        (3000, lambda: random.choice([1, 10, 50, 100, 500]), "__プラマイ３０００ 自販機の下の小銭あげますで賞！！！__"),
    ]

    result, amount = await evaluate_conditions(player_uuid, bot, conditions, diff, dice)

    kokko_uuid = bot.economysystem.get_kokko_uuid()

    # ベース分送金
    gatya_transfer(kokko_uuid, player_uuid, bot, amount)

    final_amount = amount
    earn_msg = ""

    if amount > 0:
        multiplier = get_premium_multiplier(bot, ctx.author)
        final_amount = int(amount * multiplier)
        sabun = final_amount - amount
        bot.economysystem.deposit(player_uuid, sabun)

        earn_msg = f"{final_amount}({amount}) ADP獲得！"
        premium_msg = f"`プレミアム倍率 x{multiplier:.2f}=1+(Lv合計/15)*0.5 増分 +{sabun}ADP`"
    else:
        earn_msg = f"{final_amount} ADP損失……"
        premium_msg = f"`悲しいねｗ`"

    if result is None:
        result = dedent(f"""
            # :game_die: {dice}
            # __チャレンジ失敗！__
        """)
    else:
        result += f"\n# {ctx.author.mention} :  {earn_msg} \n {premium_msg}"

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
                return dedent(f"""
                    # :game_die: {dice}
                    # {message}
                """), amount
    return None, 0

async def combo_bonus(ctx):
    combos = [
        combo.CHIKUCOMBO(),
        combo.BICOMBO(),
        combo.DEATHCOMBO(),
    ]
    cb = random.choices(combos,weights=[9,1,2],k=1)[0]
    result = await cb.combo_bonus(ctx)
    return result

async def infinite_combo_bonus(ctx):
    result = await combo.INFINITECOMBO().combo_bonus(ctx)
    return result

def get_premium_multiplier(bot,player):
    max_lv = 15
    lv_sum = bot.premiumsystem.get_level_sum(player)
    return 1.0 + (lv_sum / max_lv) * 0.5

def gatya_transfer(kokko_uuid, player_uuid, bot, amount):
    if amount < 0:
        bot.economysystem.withdraw(player_uuid, -amount)
        bot.economysystem.deposit(kokko_uuid, -amount)
    else:
        bot.economysystem.withdraw(kokko_uuid, amount)
        bot.economysystem.deposit(player_uuid, amount)
