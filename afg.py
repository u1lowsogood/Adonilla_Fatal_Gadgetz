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

#畳【み【して ) み【た！【み！
#エクステンションを有効化 テンション上がってきた……！
@bot.event
async def on_ready():
    await bot.load_extension('cogs.pinch.pinch')
    await bot.load_extension("cogs.reloader.reloader")
    await bot.load_extension("cogs.satujin.satujin")
    await bot.load_extension("cogs.itemfusion.itemfusion")
    await bot.load_extension("cogs.niconico_akaji.niconico_akaji")
    await bot.load_extension("cogs.gabigabikun.gabigabikun")
    await bot.load_extension("cogs.increase_uterus.increase_uterus")
    await bot.load_extension("cogs.amanda.amanda")

bot.run(TOKEN)