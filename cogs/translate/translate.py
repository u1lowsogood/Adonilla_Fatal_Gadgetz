from discord.ext import commands
import re
from googletrans import Translator

class Translate(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.translator = Translator()

    @commands.command(name="2")
    async def translate_cmd(self, ctx, dest:str= "en"):

        cmd = ctx.message
        if cmd.reference == None:
            await cmd.channel.send("このコマンドは返信内で使用してね（訳したいのを右クリック → 返信）")
            return
        
        targetmsg = await cmd.channel.fetch_message(cmd.reference.message_id)
        targetcontent = targetmsg.content
        if len(targetcontent) == 0:
            return
        
        detected = self.translator.detect(targetcontent)
        srcdest = detected.lang

        try:
            translated = self.translator.translate(targetcontent, dest=dest).text
        except:
            await cmd.channel.send("Translating error: 謎地域w")
            return
        
        await cmd.channel.send(f"```md\n# 【TRANSLATAED: {srcdest} > {dest}】\n```")
        
        await cmd.channel.send(self.fixmarkdown(translated))

    def fixmarkdown(self,content):
        return re.sub(r"``\s*`", "```", content)

async def setup(bot):
    await bot.add_cog(Translate(bot))