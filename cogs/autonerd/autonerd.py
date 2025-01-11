import discord
from discord.ext import commands
import random
import asyncio

class AutoNerd(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.sended_amount = 0
        self.next_amount = 5
        self.economysystem = self.bot.economysystem
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
            "👨‍🦰🇸 🇪 🇽",
            "🤓 👃 ",
            "🤓 ❤️ 👴 ",
            "👨‍🦰 🔪 🤓 ",
            "🤓 🫲 👴 ",
            "👶➡️🤓",
            "👶⬅️🤓",
            "🤓☝️ 🇸 🇹 🇺 🇵 🇮 🇩 ",
            "🤓☝️ 🇲 🇦 🇽 🇧 🅰️ 🇰 🔼 ",
            "💊 🤓 ",
            "👴🔪  🤓 🫀 🧠 🫁🩸 ",
            "🤓❤️‍🔥 ",
            "🤓 👓",
            "🤓 🕶️ ➡️ 😎 ",
            "🤓☝️ 🇲 🇦 🇳 🇺 🇰 🇪 🇼 ",
            "🤓 ☝️🇼 ",
            "🤓🤝 ",
            "🤓👄 ",
            "🤓➡️ 🦷 👓 😶 ",
            "🤓 🪡",
            ]

    @commands.Cog.listener(name="on_message")
    async def senryu_verdict(self,msg : discord.Message):
        if msg.author == self.bot.user or msg.author.bot or "/" in msg.content:
            return
        
        self.sended_amount += 1
        
        if self.sended_amount > self.next_amount:

            self.next_amount = random.randint(19,40)
            self.sended_amount = 0

            #choiced = random.choice(self.reactions).replace(' ', '')
            choicedindex = random.randrange(len(self.reactions))
            choiced = self.reactions[choicedindex].replace(' ', '').replace('　', '')
            for i, emoji in enumerate(choiced):
                try:
                    await msg.add_reaction(emoji)
                except discord.errors.HTTPException:
                    print("Unknown emoji:\nreaction_index:", choicedindex, "letter:", i, "emoji:", emoji)

            table = [
                ({"👴"},1500,"教授ボーナス！"),
                ({"👨‍🦰", "👧", "👱‍♀️"},500,"陽キャボーナス！"),
                ({"💰"},1000,"カツアゲボーナス！"),
            ]

            bonusmsg = ""
            amount = len(choiced)*100
            for t in table:
                if any(emoji in choiced for emoji in t[0]):
                    amount += t[1]
                    bonusmsg += f"{t[2]} +{t[1]}ADP!"

            self.economysystem.deposit(str(msg.author.id),amount)

            second = 3
            react_text = f"オタクが反応！ {amount} ADP獲得！{bonusmsg} ({second})"
            replymsg : discord.Message = await msg.reply(react_text)

            for i in range(3):
                second-=1
                react_text = f"オタクが反応！ {amount} ADP獲得！{bonusmsg} ({second})"
                await asyncio.sleep(1) 
                await replymsg.edit(content=react_text)
            await replymsg.delete()

            return

async def setup(bot):
    await bot.add_cog(AutoNerd(bot))


