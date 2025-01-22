import asyncio
import random
from typing import List

import discord

from cogs.shops.umaotoko import runner
from cogs.shops.umaotoko.logmanager import LogManager

# pylint: disable=no-member

class RaceManager:

    def __init__(self, bot, ctx):
        self.bot = bot
        self.ctx = ctx
        self.log_manager = LogManager()
        self.runners: List[runner.Runner] = [
            runner.NERD(),
            runner.TITUTUKI(),
            runner.EAGLE(),
            runner.YOUKYA_MALE(),
        ]
        random.shuffle(self.runners)
        self.jra_msg: discord.Message = None
        self.turn = 0
        self.lane_length = 15
        self.result = list()

    async def start_race(self):
        self.jra_msg = await self.ctx.send(self.make_race_message())
        await asyncio.sleep(1)
        await self.update_race_message()

        await asyncio.sleep(1)

        self.log_manager.add(" ")

        await self.update_race_message()

        for i in range(5, 0, -1):
            self.log_manager.add(f"レース開始まで あと{i}")
            await self.update_race_message()
            await asyncio.sleep(1)

        self.log_manager.add("レースが始まりました！走者、一斉に発進！")
        await self.update_race_message()

        for _ in range(50):
            await self.proceed_turn()
            await asyncio.sleep(1)

    def make_lanes(self) -> str:
        lanes = ""
        for i, runner in enumerate(self.runners):
            lane = "｜"+"".join(["ー"*self.lane_length])+"｜"
            lane += ":moneybag:" if i == len(self.runners)//2 else ""
            lane = list(lane)
            lane[runner.position+1] = runner.icon
            lane = "".join(lane)
            lanes += lane+"\n"
        return lanes

    async def proceed_turn(self):
        self.move_runners()
        self.turn += 1
        await self.update_race_message()

    def move_runners(self):
        for runner in self.runners:
            runner.run(self.log_manager)
            runner.sucide(self.log_manager)

            if runner.isgoal and not runner in self.result:
                self.result.append(runner)

    def make_race_message(self) -> str:
        race_message = "START　　　　　　　　　　　GOAL\n" 
        race_message += self.make_lanes()
        race_message += "\n\n"
        race_message += self.log_manager.format_logs(self.turn)
        return race_message

    async def update_race_message(self):
        await self.jra_msg.edit(content=self.make_race_message())