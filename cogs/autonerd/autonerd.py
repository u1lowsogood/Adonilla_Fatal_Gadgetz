import discord
from discord.ext import commands
import random

class AutoNerd(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.sended_amount = 0
        self.next_amount = 5
        self.reactions = [
            "🤓💦",
            "🤓",
            "🤓🔫",
            "🤓👍",
            "🤓🖕 ",
            "🤓🫰",
            "👏🤓",
            "👴",
            "👴💦",
            "🫶 🤓",
            "🤓🇰🇦🇹🇴🇼",
            "🤓 🫳 👒",
            "👴🔪 🤓",
            "👨‍🦰👧💔🤓",
            "👱‍♀️🤏🤓",
            "🤓🙏💦",
            "🤓 🤳",
            "🤓🫴🌹",
            "💥 👊 🤓",
            "💪 🤓🍤",
            "🫷 🤓 🫸",
            "👉🤓👈",
            "🤓👉👈",
            "👈🤓👉",
            "🤓 🫵",
            "🤓 🌧️",
            "🤓 🎌",
            "🤓 👂",
            "🫵 🤓 🫴 🔥",
            "🤓👴",
            "👴📢🤓",
            "🫲  🤓  🫱",
            "💉 🤓",
            "🤓 ⚠️",
            "🤓 💬",
            "🤓 🪽",
            "🤓 🏳️",
            "💰 🤓",
            "🤓 🎸",
            "🤓🫳🀄",
            "🤓🎲",
            "🤓 🍷 🌙",
            "🤓 🪭",
            "🤓 🖕",
            "🤓 💡",
            "🤓🇸 🇪 🇽",
            "🤓🩻",
            "🪓🤓",
            "🗜️👈🤓💦",
            "🎻🤓",
            "❤️‍🩹🤓",
            "🤓👉👌",
            "🤓👉👌🇸 🇪 🇽",
            "👨‍🦰🇸 🇪 🇽"
            ]

    @commands.Cog.listener(name="on_message")
    async def senryu_verdict(self,msg : discord.Message):
        if msg.author == self.bot.user or msg.author.bot or "/" in msg.content:
            return
        
        self.sended_amount += 1
        
        if self.sended_amount > self.next_amount:

            self.next_amount = random.randint(8,20)
            self.sended_amount = 0

            #choiced = random.choice(self.reactions).replace(' ', '')
            choicedindex = random.randrange(len(self.reactions))
            choiced = self.reactions[choicedindex].replace(' ', '')

            for i, emoji in enumerate(choiced):
                try:
                    await msg.add_reaction(emoji)
                except discord.errors.HTTPException:
                    print("Unknown emoji")
                    print("reaction_index:", choicedindex, "letter:", i, "emoji:", emoji)

            return

async def setup(bot):
    await bot.add_cog(AutoNerd(bot))


