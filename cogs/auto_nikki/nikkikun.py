import discord
import datetime
import asyncio
from discord.ext import commands
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from textwrap import dedent
from afgBot import afgBot

class Nikkikun(commands.Cog):

    def __init__(self, bot):
        self.bot : afgBot = bot
        self.model_name = "sonoisa/t5-base-japanese"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, use_fast=False)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)

    @commands.command(name="satujin",aliases=["殺人","さつじん","satuzin"])
    async def nikkikun(self, ctx : commands.Context):
        user_id = ctx.author.id
        summary = await self.get_and_summarize_messages(ctx, user_id)
        sendmsg = dedent(f"""# :scroll: {datetime.date.today()}
        {ctx.author.mention} の一日は、こんな風になりました！
        ```
        {summary}
        ```
        """)
        print(sendmsg)
        await ctx.channel.send(sendmsg)

    async def get_and_summarize_messages(self, ctx : commands.Context, user_id) -> str:
        now = datetime.datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        messages = []

        guild = await self.bot.fetch_guild(ctx.guild.id)
        channels = await guild.fetch_channels()
        text_channels = [ch for ch in channels if isinstance(ch, discord.TextChannel)]
        
        async for tc in text_channels:
            tc : discord.TextChannel 
            async for message in tc.history(limit=1000, after=today_start):
                if message.author.id == user_id:
                    messages.append(message.content)

        if not messages:
            return "今日はただ、虚空を見つめていた。"

        messages.sort(key= lambda msg : msg.created_at)
        text = " ".join(messages)

        input_ids = self.tokenizer.encode("日記風に要約: " + text, return_tensors="pt", max_length=3000, truncation=True)
        output = self.model.generate(input_ids, max_length=150, num_return_sequences=1)
        summary = self.tokenizer.decode(output[0], skip_special_tokens=True)

        return summary

async def setup(bot : afgBot):
    await bot.add_cog(Nikkikun(bot))