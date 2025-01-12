from cogs.shops.umaotoko.Model.runners import runner
import asyncio
import random
import discord

class Umaotoko():
    def __init__(self, bot, ctx):
        self.logs = ["「第百回 アドン杯」の開幕だぁ！","皆やる気は満々です！"]
        self.runners : runner.Runner= [
            runner.NERD(),
            runner.TITUTUKI(),
            runner.EAGLE(),
            runner.YOUKYA_MALE(),
        ]
        self.bot = bot
        self.ctx = ctx
        self.jra_msg = None
        random.shuffle(self.runners)
        
    async def start(self):
        self.jra_msg : discord.Message = await self.ctx.send(self.make_jra_message())

        for turn in range(100):
            await self.waiting_start()
            await self.proceed_turn()
            await asyncio.sleep(1)

    async def waiting_start(self):
        self.logs.append("各ランナーが位置につきました。")
        await self.update_jra_message()

        for i in range(5):
            self.logs.append(f"レース開始まで あと{5-i}")
            await self.update_jra_message()
            await asyncio.sleep(1)

    async def proceed_turn(self):
        await self.judge_and_move_runners()
        await self.update_jra_message()

    async def judge_and_move_runners(self):
        for runner_ in self.runners:
            runner_ : runner.Runner
            if runner_.judge_move():
                runner_.proceed += 1

    def get_runner(self):
        pass

    def get_side_side_runners(self):
        pass

    def make_lanes(self) -> str:
        lanes = ""
        for runner_ in self.runners:
            runner_ : runner.Runner
            lanes += runner_.draw_lane() + "\n"
        return lanes
    
    def make_logs(self) -> str:
        log_msg = "```md\n# logs"
        for i,log in enumerate(self.logs):
            log_msg += log+"\n"
            if(i > 3):
                break
        log_msg += "```"

    def make_jra_message(self) -> str:
        msg = self.make_lanes()
        msg += "\n\n"
        msg += self.make_logs()
        return msg

    async def update_jra_message(self):
        self.jra_msg = self.make_jra_message()
        await self.jra_msg.edit(self.jra_msg)