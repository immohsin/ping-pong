from enum import Enum, unique


@unique
class Stage(Enum):
    GROUP = 0
    SEMI = 1
    FINAL = 2
