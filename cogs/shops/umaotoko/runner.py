from dataclasses import dataclass, field
from abc import ABC
from textwrap import dedent
import random
from typing import Dict
from cogs.shops.umaotoko.quote import QUOTE_TYPE
from cogs.shops.umaotoko.logmanager import LogManager
from cogs.shops.umaotoko.quote import Quote

@dataclass
class Runner(ABC):
    icon: str
    name: str
    description: str
    sucidal_rate: float
    moving_probability_per_turn: float
    quotes: dict = field(default_factory=dict)
    
    position: int = 0
    isalive: bool = True
    isgoal: bool = False

    def run(self,log_manager : LogManager):
        if not self.isalive or self.isgoal:
            return
        if random.random() < self.moving_probability_per_turn / 100:
            self.position += 1
        if self.position >= 15:
            self.goal(log_manager)
    
    def goal(self, log_manager : LogManager):
        self.position = 15
        self.isgoal = True
        log_manager.add(self.get_quote(QUOTE_TYPE.WON))
        log_manager.add(self.get_quote(QUOTE_TYPE.WON,False))
    
    def sucide(self, log_manager : LogManager):
        if random.random() < self.sucidal_rate / 100:
            self.icon = ":skull:"
            self.isalive = False
            log_manager.add(self.get_quote(QUOTE_TYPE.DEATH))
            log_manager.add(self.get_quote(QUOTE_TYPE.DEATH,False))

    def get_quote(self, quote_type: QUOTE_TYPE, for_runner: bool = True) -> str:
        quotes : Quote = self.quotes.get(quote_type, None)
        if not quotes:
            return None
        if for_runner:
            return f"{self.name}「{random.choice(quotes.runner_quotes)}」"
        if quotes.commentary_quotes:
            return f"解説「{random.choice(quotes.commentary_quotes)}」"
        return None

    def get_description(self) -> str:
        return dedent(f"""
        名前：{self.name}
        説明：{self.description}
        毎ターン行動率：{self.moving_probability_per_turn} %
        希死念慮率：{self.sucidal_rate} %
        """)

class NERD(Runner):
    def __init__(self):
        super().__init__(
            icon="🤓",
            name="オタク",
            description="小走りでゴールへと向かう。",
            sucidal_rate=2,
            moving_probability_per_turn=40,
            quotes = {
                QUOTE_TYPE.DEATH: Quote(
                    runner_quotes=["もう駄目かと……ｗ","死がボキを待つかと……ｗ"],
                    commentary_quotes=["おぉっとぉ！オタクが死亡！","オタク死亡！チー牛の食べ過ぎかぁ～！？"]
                    ),
                QUOTE_TYPE.WON:Quote(
                    runner_quotes=["余裕かと……ｗ","ボキの速さには何者も付いてこれないかと……ｗ"],
                    commentary_quotes=["オタクがゴール！"]
                    ),
                }
        )

class TITUTUKI(Runner):
    def __init__(self):
        super().__init__(
            icon="🦜",
            name="チツツキ",
            description="行動率が0%の代わりに、\n「ワンワン」と鳴くたびに2～5マス前進する。",
            sucidal_rate=0,
            moving_probability_per_turn=0,
            quotes={
                QUOTE_TYPE.DEATH: Quote(
                    runner_quotes=["ワンワン"],
                    commentary_quotes=["おぉっとぉ！死んでしまったぁ！", "チツツキ選手、ここで息絶えた！"]
                ),
                QUOTE_TYPE.WON: Quote(
                    runner_quotes=["ワンワン"],
                    commentary_quotes=["チツツキ選手、ゴールしました！"]
                ),
                QUOTE_TYPE.ABILITY_ACTIVE: Quote(
                    runner_quotes=["ワンワン"]
                ),
            }
        )
        self.bowbow_rate = 30

    def run(self, log_manager : LogManager):
        if not self.isalive or self.isgoal:
            return
        if random.random() < self.bowbow_rate / 100:
            self.position += random.randrange(2,5)
            log_manager.add(self.get_quote(QUOTE_TYPE.ABILITY_ACTIVE))
        if self.position >= 15:
            self.goal(log_manager)
            

class EAGLE(Runner):
    def __init__(self):
        super().__init__(
            icon="🦅",
            name="死に鷹",
            description="空高く走る。上下1レーンの希死念慮率を吸い取る。",
            sucidal_rate=5,
            moving_probability_per_turn=70,
        )

class YOUKYA_MALE(Runner):
    def __init__(self):
        super().__init__(
            icon="👨‍🦰",
            name="陽キャ（男）",
            description="同じ位置に３ターン以上いた他ランナーを殺す。",
            sucidal_rate=0,
            moving_probability_per_turn=70,
        )

class YOUKYA_FEMALE(Runner):
    def __init__(self):
        super().__init__(
            icon="👩‍🦰",
            name="陽キャ（女）",
            description=dedent("""
            👨‍🦰陽キャ（男）が自分より先にいる場合、必ず1マス進む
            👨‍🦰陽キャ（男）より3マス以上離れるとメンヘラ化する
            """),
            sucidal_rate=0,
            moving_probability_per_turn=40,
        )

class KYOUJU(Runner):
    def __init__(self):
        super().__init__(
            icon="👴",
            name="教授",
            description=dedent("""
            周囲に🦅、または人間が居る場合、希死念慮率を付与する。
            🤓🦅の場合、割合が増加する。
            """),
            sucidal_rate=0,
            moving_probability_per_turn=40,
        )
