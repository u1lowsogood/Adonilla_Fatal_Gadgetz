from textwrap import dedent
import random
import asyncio
import inspect
import cogs.yoroduya_yuichi.combo as combo

async def use_item(bot, ctx, ticket_multiplier = 1):

    die_emoji = ":game_die:"
    
    if ticket_multiplier == 2:
        die_emoji = ":diamond_shape_with_a_dot_inside:"
    elif ticket_multiplier == 8:
        die_emoji = ":rosette:"
    elif ticket_multiplier == 32:
        die_emoji = ":moneybag: :nerd: :moneybag: "

    target = random.randint(0, 9999)
    await ctx.reply(dedent(f"""
        {ctx.author.mention} が１万分の１の確率で全財産チャレンジ！
        サイコロで **__ {target} __** の目が出たらチャレンジ成功！
    """))
    await asyncio.sleep(1)
    await ctx.send(f"# {die_emoji} ドゥルルルル……")
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
        (250, lambda: combo_bonus(ctx), "__:moneybag: ジャックポット終了:moneybag: ！__"),
        (1000, lambda: kokko_balance // 9000, "__:moneybag:プラマイ１０００ 健闘賞！！！:moneybag:__"),
        (3000, lambda: random.choice([1, 10, 50, 100, 500]), "__プラマイ３０００ 自販機の下の小銭あげますで賞！！！__"),
    ]

    result, amount = await evaluate_conditions(player_uuid, bot, conditions, diff, dice, die_emoji)
    
    origin_amount = amount

    amount *= ticket_multiplier

    kokko_uuid = bot.economysystem.get_kokko_uuid()

    # ベース分送金
    gatya_transfer(kokko_uuid, player_uuid, bot, amount)

    final_amount = amount
    earn_msg = ""

    ticket_multiplier_msg = f"x{ticket_multiplier} チケット倍率！" if ticket_multiplier > 1 else ""

    if amount > 0:
        premium_multiplier = get_premium_multiplier(bot, ctx.author)
        final_amount = int(amount * premium_multiplier)
        sabun = final_amount - amount
        bot.economysystem.deposit(player_uuid, sabun)

        earn_msg = f"{final_amount}({origin_amount}{ticket_multiplier_msg}) ADP獲得！"
        premium_msg = f"`チケット倍率 x{ticket_multiplier:.2f} プレミアム倍率 x{premium_multiplier:.2f}=1+(Lv合計/15)*0.5 プレミアム増分 +{sabun}ADP`"
    else:
        earn_msg = f"{final_amount}({ticket_multiplier_msg}) ADP損失……"
        premium_msg = f"`悲しいねｗ`"

    if result is None:
        result = dedent(f"""
            # {die_emoji} {dice}
            # __チャレンジ失敗！__
        """)
    else:
        result += f"\n# {ctx.author.mention} :  {earn_msg} \n {premium_msg}"

    await ctx.reply(result)

async def evaluate_conditions(player_uuid, bot, conditions, diff, dice, die_emoji):
    for threshold, action, message in conditions:
        if diff <= threshold:
            if action:
                result = action()
                if inspect.isawaitable(result):
                    amount = await result
                else:
                    amount = result
                return dedent(f"""
                    # {die_emoji} {dice}
                    # {message}
                """), amount
    return None, 0

async def combo_bonus(ctx):
    combos = [
        combo.CHIKUCOMBO(),
        combo.BICOMBO(),
        combo.DEATHCOMBO(),
    ]
    cb = random.choices(combos,weights=[9,1,3],k=1)[0]
    result = await cb.combo_bonus(ctx)
    return result

async def infinite_combo_bonus(ctx):
    combos = [
        combo.INFINITECOMBO(),
        combo.INFINITE_DEATH_COMBO(),
    ]
    cb = random.choices(combos,weights=[10,2],k=1)[0]
    result = await cb.combo_bonus(ctx)
    return result

def get_premium_multiplier(bot,player):
    max_lv = 15
    lv_sum = bot.premiumsystem.get_level_sum(player)
    return 1.0 + (lv_sum / max_lv) * 0.5

def gatya_transfer(kokko_uuid, player_uuid, bot, amount):
    if amount < 0:
        if bot.economysystem.get_balance(player_uuid) < -amount:
            amount = bot.economysystem.get_balance(player_uuid)
        bot.economysystem.withdraw(player_uuid, -amount)
        bot.economysystem.deposit(kokko_uuid, -amount)
    else:
        hikidasikin = amount
        if bot.economysystem.get_balance(kokko_uuid) < amount:
            hikidasikin = bot.economysystem.get_balance(kokko_uuid)
        bot.economysystem.withdraw(kokko_uuid, hikidasikin)
        bot.economysystem.deposit(player_uuid, amount)
