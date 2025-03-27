from discord.ext import commands
import random
from enum import Enum
import os
import asyncio
import discord
from textwrap import dedent

class Author(Enum):
    SORA = {"dir": "/sorara", "name": "そら"}
    HARUTO = {"dir": "/haruton", "name": "はると"}
    
class QUOTETYPE(Enum):
    TAUNT = "/taunt"
    LOSE = "/lose"
    WIN = "/win"

class Player:
    def __init__(self, author, max_damage = 30):
        self.root = "./cogs/sorakun_chatfight/quotes"
        self.author: Author = author
        self.max_health = 100
        self.health = self.max_health
        self.max_damage = max_damage
        self.charging_damage = []

    async def taunt(self, ctx: commands.Context, withgauge = False):
        taunt = self.get_random_quote(QUOTETYPE.TAUNT)
        if withgauge:
            await ctx.send(content=self.health_gauge(), file=discord.File(taunt))
        else:
            await ctx.send(file=discord.File(taunt))

    def charge_damage(self):
        damage = random.randint(1, self.max_damage)
        self.charging_damage.append(damage)

    async def attack(self, ctx: commands.Context, opponent: "Player"):
        total_damage = sum(self.charging_damage)
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

class SORAFIGHT(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.isplaying = False

    @commands.command(aliases=["そらくんチャットファイト"])
    async def sorakun(self, ctx: commands.Context, amount : int = 100):
        if self.isplaying:
            return
        self.isplaying = True

        sora = Player(Author.SORA,10)
        haruto = Player(Author.HARUTO)

        await ctx.send("たいへーん！そらくんとはるとくんが喧嘩を始めちゃった……！")

        await sora.taunt(ctx,True)
        await haruto.taunt(ctx,True)

        await asyncio.sleep(2)
        await ctx.send("どちらが勝つか、見守ってあげよう！")
        await asyncio.sleep(1)

        current_attacker = random.choice([sora, haruto])
        opponent = haruto if current_attacker == sora else sora

        while True:
            tauntflag = False
            next_attacker = random.choice([sora, haruto])
            
            if next_attacker != current_attacker:
                total_damage = sum(current_attacker.charging_damage)
                if total_damage > 0:
                    await asyncio.sleep(1)
                    current_attacker.attack(ctx, opponent)

                    if opponent.health <= 0:
                        break
                
                current_attacker = next_attacker
                opponent = haruto if current_attacker == sora else sora
                tauntflag = True

            await asyncio.sleep(random.randint(0, 1))
            async with ctx.typing():
                await asyncio.sleep(random.randint(1, 3))
            
            current_attacker.charge_damage()
            await current_attacker.taunt(ctx,tauntflag)
            tauntflag = False
        
        await self.endroll(ctx, current_attacker, opponent)
        
        self.isplaying = False

    async def endroll(self, ctx : commands.Context, winner:Player, loser:Player):
        await asyncio.sleep(2)
        await ctx.send("おっと……？")
        await asyncio.sleep(2)
    
        win_quote_path = winner.get_random_quote(QUOTETYPE.WIN)
        await ctx.send(content=winner.health_gauge(), file=discord.File(win_quote_path))
        await ctx.send(f"どうやら、{winner.author.value['name']}くんの勝利みたい！")

        await asyncio.sleep(2)
        lose_quote_path = loser.get_random_quote(QUOTETYPE.LOSE)
        await ctx.send(content=loser.health_gauge(),file=discord.File(lose_quote_path))
        await ctx.send(f"あらあら…… {loser.author.value['name']}くん、泣いちゃった！")

async def setup(bot):
    await bot.add_cog(SORAFIGHT(bot))
