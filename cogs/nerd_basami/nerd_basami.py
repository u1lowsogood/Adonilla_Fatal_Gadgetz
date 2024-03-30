from discord.ext import commands

class NerdBasami(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["NerdBasami","オタク挟み","OtakuHasami","OtakuBasami","otabasami","オタ挟み","おたばさみ"])
    async def NerdHasami(self, ctx, hasami="🤓"):
        cmd = ctx.message
        if cmd.reference == None:
            await cmd.channel.send("このコマンドは返信内で使用してね（右クリック → 返信）")
            return
        
        targetmsg = await cmd.channel.fetch_message(cmd.reference.message_id)
        sendmsg = hasami + hasami.join(targetmsg.content) + hasami

        await ctx.send(sendmsg[:2000])

async def setup(bot):
    await bot.add_cog(NerdBasami(bot))