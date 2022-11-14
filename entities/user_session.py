from datetime import datetime
from typing import NamedTuple

from common import USER_TIMEOUT_SECONDS

from .difficulty_level import DifficultyLevel
from .game_settings import GameSettings
from .interaction_state import InteractionState


class Score(NamedTuple):
    total: int
    wins: int
    losses: int


class UserSession:
    def __init__(self, user_id: int, user_name: str) -> None:
        self.user_id = user_id
        self.user_name = user_name
        self._interaction_state = InteractionState.UNSPECIFIED
        self._game_settings = GameSettings.get_new_default()
        self._game_candies_left = None
        self._score = Score(0, 0, 0)
        self.update_last_activity()

    def update_last_activity(self):
        self._last_activity = datetime.now()

    @property
    def is_online(self) -> bool:
        return (datetime.now()-self._last_activity).total_seconds() < USER_TIMEOUT_SECONDS

    @property
    def interaction_state(self) -> InteractionState:
        return self._interaction_state

    @interaction_state.setter
    def interaction_state(self, value):
        self._interaction_state = value

    @property
    def game_settings(self) -> GameSettings:
        return self._game_settings

    def set_difficulty(self, difficulty: DifficultyLevel):
        self.game_settings.difficulty = difficulty

    def set_candies_total(self, value):
        self.game_settings.candies_total = value

    def set_candies_per_turn(self, value):
        self.game_settings.candies_per_turn = value

    @property
    def game_candies_left(self) -> int:
        return self._game_candies_left

    def withdraw_candies(self, how_many: int):
        assert self._game_candies_left > how_many, 'Unacceptable qty of candies to withdraw.'
        self._game_candies_left -= how_many

    @property
    def is_in_game(self) -> bool:
        return self._game_candies_left is not None

    def new_game(self, whose_first: InteractionState) -> None:
        assert whose_first in [InteractionState.GAME_AI_TURN,
                               InteractionState.GAME_USER_TURN], f'Wrong argument value: whose_first cannot be \'{whose_first}\'!'
        self.update_last_activity()
        self._game_candies_left = self.game_settings.candies_total
        self._interaction_state = whose_first

    def game_over(self, is_user_winner) -> None:
        assert self.is_in_game, f'User {self.user_id} must be in active game to execute game_over() mtod.'
        self.update_last_activity()

        score = self._score
        if is_user_winner:
            self._score = Score(score.total+1, score.wins+1, score.losses)
        else:
            self._score = Score(score.total+1, score.wins, score.losses+1)

        self._game_candies_left = None
        self._interaction_state = InteractionState.UNSPECIFIED

    @property
    def score(self) -> Score:
        return self._score
