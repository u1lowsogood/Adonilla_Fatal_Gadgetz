from discord.ext import commands

class Reloader(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="afgreload")
    async def reload(self, ctx, arg=None):
        #extensions = ["satujin"]

        extensions = self.bot.extensions.keys()
        for extension in extensions:
            await ctx.send("extension: " + extension + " を リロードしましたｗ")
            await self.bot.reload_extension(extension)

async def setup(bot):
    await bot.add_cog(Reloader(bot))