from discord.ext import commands
import discord
import asyncio
import random
import os

from cogs.sorakun_chatfight.author import Author
from cogs.sorakun_chatfight.quotetype import QUOTETYPE

class Player:
    def __init__(self, author, min_damage = 1,max_damage = 30):
        self.root = "./cogs/sorakun_chatfight/quotes"
        self.author: Author = author
        self.max_health = 100
        self.health = self.max_health
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.charging_damage = []
        self.show_health_gauge = True

    async def taunt(self, ctx: commands.Context):
        taunt = self.get_random_quote(QUOTETYPE.TAUNT)
        if self.show_health_gauge:
            await ctx.send(content=self.health_gauge(), file=discord.File(taunt))
            self.show_health_gauge = False
        else:
            await ctx.send(file=discord.File(taunt))

    def charge_damage(self):
        damage = random.randint(self.min_damage, self.max_damage)
        self.charging_damage.append(damage)

    async def attack(self, ctx: commands.Context, opponent: "Player"):
        total_damage = sum(self.charging_damage)

        if total_damage <= 0:
            return
    
        await asyncio.sleep(1)
        opponent.health -= total_damage
        await ctx.send(f"{opponent.author.value['name']}くんに **{total_damage} ダメージ！** `(={ '+'.join(map(str, self.charging_damage)) })`")
        self.charging_damage.clear()

    def health_gauge(self):
        filled_count = round((self.health / self.max_health) * 10)
        filled = "■" * filled_count 
        empty = "-" * (10 - filled_count)
        return dedent(f"""```md
|{filled}{empty}|({0 if self.health < 0 else self.health}/{self.max_health})
```""")

    def get_random_quote(self, quote_type: QUOTETYPE):
        dir_path = self.root + self.author.value["dir"] + quote_type.value
        files = os.listdir(dir_path)
        random_quote = os.path.join(dir_path, random.choice(files))
        return random_quote