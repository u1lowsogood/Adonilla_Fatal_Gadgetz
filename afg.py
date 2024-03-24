#!/usr/bin/python
# -*- coding: utf-8 -*-
import asyncio
from typing import Any, Coroutine, Optional
import discord
from discord.ext import tasks, commands
import sys

args = sys.argv
if len(args) != 4:
    print("ｳﾝﾁｗｳﾝﾁｗｳﾝﾁｗｳﾝﾁｗｳﾝﾁｗｳﾝﾁｗｳﾝﾁｗｳﾝﾁｗ（訳：引数周辺のアレがアレっぽいワｗ（笑）")
    sys.exit(1)

TOKEN = args[1]

#インテンツ登録【してみた！)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

class afgBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="/",intents=intents)
        self._sqluser = args[2]
        self._sqlpassword = args[3]
    
    @property
    def sqluser(self):
        return self._sqluser
    
    @property
    def sqlpassword(self):
        return self._sqlpassword
    
        
bot = afgBot()

#上から読み込まれるからデバッグしたい新規機能は上から追加したほうがいいかも？
cogz = [
    "cogs.translate.translate",
    "cogs.pinch.pinch",
    "cogs.reloader.reloader",
    "cogs.satujin.satujin",
    "cogs.itemfusion.itemfusion",
    "cogs.niconico_akaji.niconico_akaji",
    "cogs.gabigabikun.gabigabikun",
    "cogs.increase_uterus.increase_uterus",
    "cogs.amanda.amanda",
    "cogs.message_register.message_register",
    "cogs.selfmention.selfmention",
    "cogs.generatemap.generatemap",
    "cogs.infinite_kenson.infinite_kenson",
    "cogs.random_music.randommusic",
    "cogs.daibendori.daibendori",
    "cogs.yugamismile.yugamismile",
    "cogs.otanishohei.otanishohei",
    "cogs.uikittest.uikittest",
    "cogs.u1quiz.u1quiz",
    "cogs.deathsenryu.deathsenryu",
    "cogs.n.n",
    "cogs.autonerd.autonerd",
    "cogs.utsu.utsu",
    "cogs.word.word",
    "cogs.fakegoogle.fakegoogle"
        ]

#畳【み【して ) み【た！【み！
#エクステンションを有効化 テンション上がってきた……！
@bot.event
async def on_ready():
    for kog in cogz:
        await bot.load_extension(kog)
        print(f"{kog} was loaded!")
    print(f"< all cogs were successfully loaded! >\n")

bot.run(TOKEN)