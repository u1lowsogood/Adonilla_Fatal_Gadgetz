#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from afgBot import afgBot

def main():
    args = sys.argv
    if len(args) != 4:
        print("引数をもっといい感じに指定してね")
        sys.exit(1)

    TOKEN = args[1]
    sqluser = args[2]
    sqlpassword = args[3]

    bot = afgBot(TOKEN, sqluser, sqlpassword)

    cogz = [
        "cogs.textcooler.textcooler",
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
        "cogs.shops.u1chinko.u1chinko",
        "cogs.shops.umaotoko.umaotoko_command",
        "cogs.exp.exp_commands",
        "cogs.exp.exp_listeners",
        "cogs.recaliculate_birthday.tanjohbi",
        "cogs.metronome.metro",
        "cogs.sorakun_chatfight.sorafight"
        #"cogs.depressed_battle.depressed_battle",
        ]

    @bot.event
    async def on_ready():
        for kog in cogz:
            await bot.load_extension(kog)
            print(f"{kog} was loaded!")
        print("< all cogs were successfully loaded! >\n")

    bot.run(TOKEN)

if __name__ == "__main__":
    main()