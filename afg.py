#!/usr/bin/python
# -*- coding: utf-8 -*-
import asyncio
from typing import Any, Coroutine, Optional
import discord
from discord.ext import tasks, commands
import sys
from cogs.adonilla_eco_system.economysystem import EconomySystem
from cogs.shops.shops.shopsystem import ShopSystem
from cogs.shops.premium_shop.premiumsystem import PremiumSystem

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
intents.voice_states = True

class afgBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="/",intents=intents)
        self._sqluser = args[2]
        self._sqlpassword = args[3]
        self._economysystem = EconomySystem(args[2], args[3])
        self._shopsystem = ShopSystem(args[2], args[3], self.economysystem)
        self._premiumsystem = PremiumSystem()
    
    @property
    def sqluser(self):
        return self._sqluser
    
    @property
    def sqlpassword(self):
        return self._sqlpassword
    
    @property
    def economysystem(self):
        return self._economysystem
    
    @property
    def shopsystem(self):
        return self._shopsystem
    
    @property
    def premiumsystem(self):
        return self._premiumsystem
    
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
    "cogs.fakegoogle.fakegoogle",
    "cogs.kyuutou.kyuutou",
    "cogs.randomhibari.randomhibari",
    "cogs.whatdoyouthinkguys.whatdoyouthinkguys",
    "cogs.autovcstatus.autovcstatus",
    "cogs.nerd_basami.nerd_basami",
    "cogs.movingutsu.movingutsu",
    "cogs.damarasekun.damarasekun",
    "cogs.kintamaoukoku.kintamaoukoku",
    "cogs.curse.curse",
    "cogs.todorate.todorate",
    "cogs.convertfxtwitter.convertfxtwitter",
    "cogs.daily_bonus.daily_bonus",
    "cogs.kusodeka.kusodeka",

    "cogs.adonilla_eco_system.eco_commands",
    "cogs.shops.shops.shops",
    "cogs.shops.premium_shop.premium_shop",
    "cogs.shops.yoroduya_yuichi.yoroduya_yuichi",
    "cogs.shops.u1chinko.u1chinko"
    "cogs.shops.umaotoko.umaotoko_command"
    #"cogs.depressed_battle.depressed_battle",
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