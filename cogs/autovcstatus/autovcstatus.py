import discord
from discord.ext import commands
import random
import asyncio

class AutoVcStatus(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.statuslib=[
        "セックス中",
        "交尾中",
        "皇居攻略中",
        "家族交流中",
        "硫黄島攻略中",
        "セックス中（1/2）",
        "西方浄土",
        "殺意チャージ中",
        "エロすぎ牧場経営中",
        "@45",
        "ウンチが増えるよ！？",
        "エロ自爆マシン",
        "🤓 🤓 🤓 🤓 🤓 🤓 🤓 🤓",
        "今なら半額",
        "島流し中",
        "男子トイレ@１",
        "🤓 💩",
        "BF2042兆",
        "スレ主",
        "ガチ放尿生配信",
        "オナニー大好き祭",
        "【ご報告】",
        "あなたは18歳以上ですか？",
        "≧広告をスキップ",
        "アドンイラ記念日通話",
        "ここで一句！",
        "ドラえもんのび太の",
        "通話に入ると死亡",
        "🤓🖕 ",
        "人間牧場",
        "網走監獄",
        "↓ まんこ共",
        "アドンイラ　エロ",
        "あ",
        "#【貴方の今の発言、要約するとこのようになります。】",
        "高校生 八島恭平 総破壊",
        "最強雄筋肉チンポバトル",
        "文字ぴったん 24時間耐久",
        "出産中",
        "転生したら皇居だった件",
        "受精中",
        "米津の精液で満たされる国技館",
        "製糸工場",
        "不揃い品↓",
        "崇教真光 道場",
        "防空壕",
        "社会的に孤立",
        "GANTZの部屋",
        "深海四層",
        "振り向いてはいけない小道",
        "武力の差を感じましたか?",
        "通話を出ないと出れない通話",
        "残業",
        "寝落ち通話",
        "チャＨ",
        "エロイプ中",
        "ヤリ部屋",
        "魔女集会",
        "隠れキリシタン",
        "焼かれた故郷の村",
        "ガチエロキングダム",
        "↓毒牧場",
        "ARAM @5",
        "Valorant 勃",
        "OverWatch",
        "CreepTD配信中♡",
        "魔女集会",
        "ああああああああああｗｗ",
        "♡ｶﾞSﾁ交ｱEｸ尾Xﾒ♡",
        "ウンコ耐久レース",
        "WarRock募集！",
        "チャンネルステータスを設定♡",
        "これエロすぎない？",
        "エ配ロ信い",
        "a------",
        "履修登録中",
        ]

    @commands.Cog.listener(name="on_voice_state_update")
    async def word(self, member, before, after):
        connected: discord.VoiceChannel = after.channel
        if connected == None:
            return
        if len(connected.members) == 1:
            choicedstatus = random.choice(self.statuslib)
            await connected.edit(status=choicedstatus)

async def setup(bot):
    await bot.add_cog(AutoVcStatus(bot))