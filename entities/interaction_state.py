from enum import Enum, auto


class InteractionState(Enum):
    UNSPECIFIED = auto()
    SET_DIFFICULTY = auto()
    SET_CANDIES_TOTAL = auto()
    SET_CANDIES_PER_TURN = auto()
    GAME_AI_TURN = auto()
    GAME_USER_TURN = auto()
