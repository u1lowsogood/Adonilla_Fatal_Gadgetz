from discord.ext import commands
import random
import asyncio
import discord
from afgBot import afgBot
from textwrap import dedent
from cogs.sorakun_chatfight.playermanager import PlayerManager
from cogs.sorakun_chatfight.quotetype import QUOTETYPE

class SORAFIGHT(commands.Cog):

    def __init__(self, bot : afgBot):
        self.bot = bot
        self.economy_system = bot.system.economysystem
        self.user_playing = {}

    @commands.command(aliases=["そらくんチャットファイト"])
    async def sorakun(self, ctx: commands.Context, stake_amount : int = None):

        if stake_amount == None:
            await ctx.send("賭け金を指定してください。３倍になります。（500ADP ～）例：`/sorakun 500`")
            return
        
        if stake_amount < 500:
            await ctx.send("賭け金が不足しています！（500ADP ～）")
            return

        balance = self.economy_system.get_balance(str(ctx.author.id))
        if balance < stake_amount:
            await ctx.send(f"残高が不足しています！：{balance - stake_amount} ADP")
            return
        
        if self.user_playing.get(ctx.author.id, False):
            return
        self.user_playing[ctx.author.id] = True

        playerManager = PlayerManager()

        await ctx.send("たいへーん！そらくんとはるとくんが喧嘩を始めちゃった……！")

        await ctx.send(f"貴方の賭け金：{stake_amount} ADP。そらくん勝利時に** 3倍 **になります。 ** 負けたら全額没収。 **")

        await playerManager.players["sora"].taunt(ctx)
        await playerManager.players["haruto"].taunt(ctx)

        await asyncio.sleep(2)
        await ctx.send("どちらが勝つか、見守ってあげよう！")
        await asyncio.sleep(1)

        while True:
            playerManager.set_next_attacker_randomly()
            
            if playerManager.next_attacker != playerManager.current_attacker:
                await playerManager.current_attacker.attack(ctx, playerManager.get_opponent())

                if playerManager.get_opponent().health <= 0:
                    break
                
                playerManager.flip_attacker()

            await asyncio.sleep(random.randint(0, 1))
            async with ctx.typing():
                await asyncio.sleep(random.randint(1, 3))
            
            playerManager.current_attacker.charge_damage()
            await playerManager.current_attacker.taunt(ctx)
        
        await self.endroll(ctx, playerManager)
        await self.process_payment(ctx, playerManager, stake_amount)
        
        self.user_playing[ctx.author.id] = False

    async def endroll(self, ctx : commands.Context, playerManager: PlayerManager):

        winner = playerManager.current_attacker
        loser = playerManager.get_opponent()

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

    async def process_payment(self, ctx:commands.Context, playerManager: PlayerManager, stake_amount):

        winner = playerManager.current_attacker
        paymentmsg = ""

        if winner == playerManager.players["sora"]:
            self.bot.system.economysystem.transfer_from_kokko(str(ctx.author.id), stake_amount*2)
            paymentmsg = f"# {ctx.author.mention}、 {stake_amount*3} ADPを獲得！"
        else:
            self.bot.system.economysystem.transfer_from_kokko(str(ctx.author.id), -stake_amount)
            paymentmsg = f"# {ctx.author.mention}、 {stake_amount} ADPを失う……！"

        await ctx.send(paymentmsg)


async def setup(bot):
    await bot.add_cog(SORAFIGHT(bot))
