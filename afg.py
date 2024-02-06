#!/usr/bin/python
# -*- coding: utf-8 -*-
import asyncio
import discord
from discord.ext import tasks, commands
import sys

args = sys.argv
if len(args) != 2:
    print("ｳﾝﾁｗｳﾝﾁｗｳﾝﾁｗｳﾝﾁｗｳﾝﾁｗｳﾝﾁｗｳﾝﾁｗｳﾝﾁｗ（訳：どうやら トークンの アレ違うっぽいっすね……ｗ（笑）")
    sys.exit(1)

TOKEN = args[1]

#インテンツ登録【してみた！)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

#Bot（Clientのサブクラス）登録【してみた！)
bot = commands.Bot(command_prefix="/",intents=intents)

cogz = [
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
    "cogs.otanishohei.otanishohei"
        ]

#畳【み【して ) み【た！【み！
#エクステンションを有効化 テンション上がってきた……！
@bot.event
async def on_ready():
    for kog in cogz:
        await bot.load_extension(kog)
    
bot.run(TOKEN)