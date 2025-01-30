from discord.ext import commands
from cogs.exp.expsystem import ExpSystem
import discord 
from datetime import datetime

class EXPListeners(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.expsystem : ExpSystem = self.bot.system.expsystem
        self.base_exp_table = {
            "message_send" : 3,
            "vc_per_second" : 3/60
        }
        self.join_times = {}

    @commands.Cog.listener()
    async def on_message(self,msg : discord.Message):
        await self.expsystem.add_exp(msg.author, self.base_exp_table["message_send"])

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        if before.channel is None and after.channel is not None:
            self.join_times[member.id] = datetime.now()

        if before.channel is not None and after.channel is None:
            if member.id in self.join_times:
                join_time = self.join_times.pop(member.id)
                time_spent = datetime.now() - join_time

                exp_earned = int(self.base_exp_table["vc_per_second"] * time_spent.total_seconds())
                await self.expsystem.add_exp(member, exp_earned)

                print(f"{member.name} spent {time_spent} and earn {exp_earned} in the voice channel.")

async def setup(bot):
    await bot.add_cog(EXPListeners(bot))