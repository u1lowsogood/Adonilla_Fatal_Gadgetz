import discord
from discord.ext import commands

class METRONOME(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.path = "./cogs/metronome/sounds/"
        self.sounds = {
            "通常" : "metronome_normal.mp3",
            "お風呂場" : "metronome_bathroom.mp3",
            "ディレイ" : "metronome_delayed.mp3",
            "定規弾き" : "metronome_plucked.mp3",
            "音割れ" : "metronome_distorted.mp3",
            }

    @commands.command()
    async def metronome(self, ctx, sound_index : int = None):

        if not sound_index:
            sendmsg = "```md\n# 【音一覧】\n"
            for i, sounds in enumerate(self.sounds.keys(),1):
                sendmsg += f"{i}. {sounds}メトロノーム\n"
            sendmsg += "使用例：\n/metronome 1\n```"
            await ctx.send(sendmsg)
            return

        if not ctx.author.voice:
            await ctx.send("VCはいってから実行し（なさい）ｗ")
            return
        
        channel = ctx.author.voice.channel
        if ctx.guild.voice_client is None:
            await channel.connect()

        voice_client = ctx.guild.voice_client

        if voice_client.is_playing():
            voice_client.stop()
    
        sound_path =  self.path + list(self.sounds.values())[sound_index-1]
        source = discord.FFmpegPCMAudio(sound_path)
        voice_client.play(source)

        await ctx.send(f"{list(self.sounds.keys())[sound_index-1]}メトロノーム の音を５分間再生します（60bpm）")

async def setup(bot):
    await bot.add_cog(METRONOME(bot))
