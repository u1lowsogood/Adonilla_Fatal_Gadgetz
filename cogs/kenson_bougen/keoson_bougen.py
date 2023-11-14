from discord.ext import commands
import random

class KensonBougen(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.dict = {"死ね":"あ～……ｗ",
                     "しね":"あ～……",
                     "消えろ":"いや……w",
                     "きえろ":"いや……",
                     "ゴミ":"うーん……",
                     "ごみ":"うーん……",
                     "アホ":"そうかな",
                     "あほ":"そうだね",
                     "ドジ":"・・・",
                     "どじ":"...",
                     "まぬけ":"いえいえ",
                     "マヌケ":"いえいえｗ",
                     "障害者":"うんうん",
                     "障害":"ウンウン",
                     "ガイジ":"ｳﾝｳﾝ",
                     "ブス":"そうかな？",
                     "ブサイク":"そうかなぁ？",
                     "ハゲ":"あーわかるかも……",
                     "デブ":"分かるよ",
                     "gap":"そうだよねえ",
                     "クソ":"いやぁ……",
                     "くそ":"え～～ｗ",
                     "ウスノロ":"でも",
                     "カス":"あ～～～",
                     "チンコ":"はいはいはいはいｗ",
                     "マンコ":"そうだよな～",
                     "チンカス":"いやぁ………",
                     "自殺しろ":"共感するわｗ",
                     }
        
    @commands.command(aliases=["暴言謙遜","b2k","bougen2kenson"])
    async def bougenkenson(self, ctx):
        if ctx.message.reference == None:
            await ctx.send("このコマンドは返信\n # と一緒に\n # 利用してみてねｗ←ｗ")
            return
        msg = ctx.message.reference.
        await ctx.send(sendarg)

    @commands.command(aliases=["謙遜暴言","k2b","kenson2bougen"])
    async def kensonbougen(self, ctx):
        if ctx.message.reference == None:
            await ctx.send("このコマンドは返信\n # と一緒に\n # 利用してみてねｗ←ｗ")
            return
        await ctx.send(sendarg)

async def setup(bot):
    await bot.add_cog(KensonBougen(bot))