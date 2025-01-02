from discord.ext import commands
import discord
import re

class Convert2Fxtwitter(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name="on_message")
    async def on_message(self, msg: discord.Message):
        if msg.author == self.bot.user or msg.author.bot:
            return
        
        twitter_url_pattern = r"https?://(?:www\.)?(x|twitter)\.com/(\w+)/status/(\d+)"
        match = re.search(twitter_url_pattern, msg.content)
        
        if match:
            await msg.delete()
            username = match.group(2)
            status_id = match.group(3)
            fx_twitter_url = f"https://fxtwitter.com/{username}/status/{status_id}"
            await msg.channel.send(f"> from {msg.author.nick or msg.author.name}")
            await msg.channel.send(f"{fx_twitter_url}")

async def setup(bot):
    await bot.add_cog(Convert2Fxtwitter(bot))
