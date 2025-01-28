from enum import Enum
from typing import List, Optional
from dataclasses import dataclass

class QUOTE_TYPE(Enum):
    DEATH = 1
    WON = 2
    ABILITY_ACTIVE = 3

@dataclass
class Quote:
    runner_quotes: List[str]
    commentary_quotes: Optional[List[str]] = None