from discord.ext import commands
from cogs.exp.expsystem import ExpSystem
import discord 
from datetime import datetime
import re

class EXPListeners(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.expsystem: ExpSystem = self.bot.system.expsystem
        self.base_exp_table = {
            "message_send": 1,
            "message_exp_per_char" : 1 / 20,
            "message_has_picture": 6,
            "message_mentioned": 6,
            "message_word_bonus": 5,
            "vc_per_second": 3 / 60
        }
        self.join_times = {}
        self.special_words = {"チン", "マン","エロ","ンコ","狂","殺","悪","オタク"}

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.bot or msg.content.startswith("/"):
            return

        total_exp = 0
        total_exp += self.base_exp_table["message_send"]

        if msg.attachments:
            total_exp += self.base_exp_table["message_has_picture"]

        if msg.mentions:
            for mentioned in msg.mentions:
                await self.expsystem.add_exp(mentioned, self.base_exp_table["message_mentioned"])
            total_exp += self.base_exp_table["message_mentioned"]

        word_count = sum(1 for word in self.special_words if word in msg.content)
        total_exp += word_count * self.base_exp_table["message_word_bonus"]
        total_exp += 1 + round(len(msg.content) * self.base_exp_table["message_exp_per_char"])

        lv_before = await self.expsystem.get_status(msg.author)
        lv_before = lv_before["level"]
        await self.expsystem.add_exp(msg.author, total_exp)
        lv_after = await self.expsystem.get_status(msg.author)
        lv_after = lv_after["level"]

        if lv_before != lv_after:
            lvup_emoji = ["🇱", "🇻", "🇺", "🇵"]
            for emoji in lvup_emoji:
                await msg.add_reaction(emoji)

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