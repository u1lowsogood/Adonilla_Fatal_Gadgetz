from dataclasses import dataclass, field
from cogs.shops.umaotoko import runner
from typing import List

@dataclass
class result:
    rank: List[runner.Runner] = field(default_factory=list)