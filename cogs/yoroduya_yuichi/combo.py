import random
import asyncio
import abc

class Combo(metaclass=abc.ABCMeta):
    def __init__(self, bonus_steps, gif, combo_start_msg):
        self.bonus_steps = bonus_steps
        self.gif = gif
        self.combo_start_msg = combo_start_msg

    async def combo_bonus(self, ctx):
        bonus_iterator = iter(self.bonus_steps)
        current_range, current_bonus, decorator = next(bonus_iterator)

        total_bonus = 0
        combo_count = random.randint(4, 13)

        await ctx.reply(self.combo_start_msg)

        for i in range(combo_count):
            if i + 1 > current_range:
                current_range, current_bonus, decorator = next(bonus_iterator)

            combomsg = f"{decorator[0]}{ctx.author.mention} {i + 1} COMBO! :moneybag:+{current_bonus} ADP{decorator[1]}"
            await ctx.send(combomsg)
            await asyncio.sleep(1)
            total_bonus += current_bonus

        return total_bonus

class CHIKUCombo(Combo):
    def __init__(self):
        bonus_steps = [
            (3, 100, ["", ""]),
            (6, 300, ["**", "**"]),
            (9, 600, ["__**", "**__"]),
            (12, 1200, ["## __", "__"]),
            (15, 5000, ["# __*MAX COMBO！！！", "*__"]),
        ]
        gif = "https://media1.tenor.com/m/0YSqS0ixtm4AAAAd/pon.gif"
        combo_start_msg = f"# !!:moneybag: プラマイ５００JACKPOT :moneybag: スタート!!\n{gif}"
        super().__init__(bonus_steps, gif, combo_start_msg)

class BICOMBO(Combo):
    def __init__(self):
        bonus_steps = [
            (3, 500, ["", ""]),
            (6, 700, ["**", "**"]),
            (9, 1000, ["__**", "**__"]),
            (12, 1500, ["## __", "__"]),
            (15, 3000, ["# __*MAX COMBO！！！", "*__"]),
        ]
        gif = "https://media.discordapp.net/attachments/366193178568818688/898551298566283314/test.gif"
        combo_start_msg = f"# !!:moneybag: プラマイ５００JACKPOT :moneybag: スタート!!\n{gif}"
        super().__init__(bonus_steps, gif, combo_start_msg)

class DEATHCOMBO(Combo):
    def __init__(self):
        bonus_steps = [
            (3, 100, ["", ""]),
            (6, 300, ["**", "**"]),
            (9, 600, ["__**", "**__"]),
            (12, 1200, ["## __", "__"]),
            (15, 5000, ["# __*MAX COMBO！！！", "*__"]),
        ]
        gif = "https://media.discordapp.net/attachments/366193178568818688/1216671641451499520/nerd_1.gif"
        combo_start_msg = f"# !!:skull:  プラマイ５００死のジャックポット :skull:  スタート!!\n{gif}"
        super().__init__(bonus_steps, gif, combo_start_msg)

    async def combo_bonus(self, ctx):
        bonus_iterator = iter(self.bonus_steps)
        current_range, current_bonus, decorator = next(bonus_iterator)

        total_bonus = 0
        combo_count = random.randint(4, 13)

        await ctx.reply(self.combo_start_msg)

        for i in range(combo_count):
            if i + 1 > current_range:
                current_range, current_bonus, decorator = next(bonus_iterator)

            combomsg = f"{decorator[0]}{ctx.author.mention} {i + 1} COMBO! :skull:-{current_bonus} ADP{decorator[1]}"
            await ctx.send(combomsg)
            await asyncio.sleep(1)
            total_bonus -= current_bonus

        return total_bonus