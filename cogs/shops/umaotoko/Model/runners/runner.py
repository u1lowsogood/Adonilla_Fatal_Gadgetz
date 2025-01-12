import dataclasses
from abc import ABC, abstractmethod
from textwrap import dedent
import random

@dataclasses.dataclass
class Runner(ABC):
    icon : str
    name: str
    description : str

    sucidal_rate : float
    moving_probability_per_turn : float

    proceed : int = 0

    def draw_lane(self) -> str:
        lane = "｜"
        for i in range(15):
            lane += "ー" if i == self.proceed else self.icon
        lane += "｜"
        return lane

    def judge_move(self) -> bool:
        if random.random() < self.moving_probability_per_turn:
            return True
        return False
    
    def get_description(self) -> str:
        msg = dedent(f"""
        名前：{self.name}
        説明：{self.description}
        毎ターン行動率：{self.moving_probability_per_turn} %
        希死念慮率：{self.sucidal_rate} %
        """)
        return msg

class NERD(Runner):
    icon = "🤓"
    name = "オタク"
    description = "小走りでゴールへと向かう。"

    sucidal_rate = 2
    moving_probability_per_turn = 5

class TITUTUKI(Runner):
    icon = "🦜"
    name = "チツツキ"
    description = dedent(f"""
    「ワンワン」と鳴く旅に２～５マス前進する。
    """)

    sucidal_rate = 0
    moving_probability_per_turn = 0

class EAGLE(Runner):
    icon = "🦅"
    name = "死に鷹"
    description = "空高く走る。上下１レーンの希死念慮率を吸い取る。"

    sucidal_rate = 5
    moving_probability_per_turn = 70

class YOUKYA_MALE(Runner):
    icon = "🦆"
    name = "鴨"
    description = "自身へのベット金額に応じて動く速度が低下する。"

    sucidal_rate = 0.5
    moving_probability_per_turn = 70



class YOUKYA_MALE(Runner):
    icon = "👨‍🦰"
    name = "陽キャ（男）"
    description = ""

    sucidal_rate = 0
    moving_probability_per_turn = 70

class YOUKYA_FEMALE(Runner):
    icon = "👩‍🦰"
    name = "陽キャ（女）"
    description = dedent(f"""
    👨‍🦰陽キャ（男）が自分より先にいる場合、必ず１マス進む
    👨‍🦰陽キャ（男）より３マス以上離れるとメンヘラ化する
    """)

    sucidal_rate = 0
    moving_probability_per_turn = 40

class KYOUJU(Runner):
    icon = "👴"
    name = "教授"
    description = dedent(f"""
    周囲に🦅、または人間が居る場合、希死念慮率を付与する。
    🤓🦅の場合、割合が増加する。
    """)

    sucidal_rate = 0
    moving_probability_per_turn = 40
