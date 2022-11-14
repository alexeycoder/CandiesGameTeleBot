from enum import Enum

from common import DIFFICULTY_EASY_TXT, DIFFICULTY_HARD_TXT


class DifficultyLevel(Enum):
    EASY = DIFFICULTY_EASY_TXT
    HARD = DIFFICULTY_HARD_TXT
