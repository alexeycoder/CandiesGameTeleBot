from .difficulty_level import DifficultyLevel
from common import CANDIES_TOTAL_DEFAULT, CANDIES_PER_TURN_DEFAULT, DIFFICUTLY_DEFAULT


class GameSettings:
    __slots__ = ('candies_total', 'candies_per_turn', 'difficulty')

    def __init__(self, candies_total: int, candies_per_turn: int, difficulty: DifficultyLevel) -> None:
        self.candies_total = candies_total
        self.candies_per_turn = candies_per_turn
        self.difficulty = difficulty

    def __str__(self) -> str:
        return f'GameState(candies total={self.candies_total}, per run={self.candies_per_turn}, difficulty={self.difficulty})'

    @classmethod
    def get_new_default(cls):
        return cls(candies_total=CANDIES_TOTAL_DEFAULT,
                   candies_per_turn=CANDIES_PER_TURN_DEFAULT,
                   difficulty=DifficultyLevel(DIFFICUTLY_DEFAULT))
