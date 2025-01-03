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
        matches = list(re.finditer(twitter_url_pattern, msg.content))

        if not matches:
            return

        if "||" in msg.content:
            parts = re.split(r"(\|\|.*?\|\|)", msg.content)
            reconstructed = ""
            for part in parts:
                if part.startswith("||") and part.endswith("||"):
                    inner_matches = re.finditer(twitter_url_pattern, part)
                    updated_part = part
                    for match in inner_matches:
                        username = match.group(2)
                        status_id = match.group(3)
                        fx_twitter_url = f"https://fxtwitter.com/{username}/status/{status_id}"
                        updated_part = updated_part.replace(match.group(0), fx_twitter_url)
                    reconstructed += updated_part
                else:
                    updated_part = part
                    for match in matches:
                        username = match.group(2)
                        status_id = match.group(3)
                        fx_twitter_url = f"https://fxtwitter.com/{username}/status/{status_id}"
                        updated_part = updated_part.replace(match.group(0), fx_twitter_url)
                    reconstructed += updated_part
            updated_content = reconstructed
        else:

            updated_content = msg.content
            for match in matches:
                username = match.group(2)
                status_id = match.group(3)
                fx_twitter_url = f"https://fxtwitter.com/{username}/status/{status_id}"
                updated_content = updated_content.replace(match.group(0), fx_twitter_url)

        await msg.delete()

        await msg.channel.send(f"> from {msg.author.nick or msg.author.name}")
        if msg.reference:
            ref_msg = await msg.channel.fetch_message(msg.reference.message_id)
            await ref_msg.reply(updated_content)
        else:
            await msg.channel.send(updated_content)

async def setup(bot):
    await bot.add_cog(Convert2Fxtwitter(bot))
