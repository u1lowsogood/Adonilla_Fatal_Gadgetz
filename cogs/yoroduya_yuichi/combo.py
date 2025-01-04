import random
import asyncio
import abc

class Combo(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def combo_bonus(self,ctx):
        raise NotImplementedError()
class NormalCombo:

    def __init__(self):


    async def combo_bonus(self,ctx):
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