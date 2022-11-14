import itertools
import random

import common
from entities.difficulty_level import DifficultyLevel
from entities.game_settings import GameSettings
from entities.interaction_state import InteractionState
from entities.user_session import UserSession

ERR_EXISTING_USER_REQ = 'This mtod is not assumed to be called for new users.'

users: dict[int, UserSession] = {}


def is_new_user(user_id: int) -> bool:
    return user_id not in users


def add_new_user(user_id: int, user_name: str) -> UserSession:
    user_session = UserSession(user_id, user_name)
    users[user_id] = user_session
    return user_session


def __assert_user_exists(user_id: int):
    assert user_id in users, ERR_EXISTING_USER_REQ


def get_existing_user_session(user_id: int) -> UserSession:
    __assert_user_exists(user_id)
    return users.get(user_id)


def update_user_activity(user_id: int):
    user_session = get_existing_user_session(user_id)
    user_session.update_last_activity()


def get_user_game_settings(user_id: int) -> GameSettings:
    user_session = get_existing_user_session(user_id)
    return user_session.game_settings


def is_user_playing(user_interaction_state: InteractionState) -> bool:
    return user_interaction_state in [InteractionState.GAME_AI_TURN, InteractionState.GAME_USER_TURN]


def user_been_away_too_long(user_id: int) -> bool:
    user_session = get_existing_user_session(user_id)
    return not user_session.is_online


def user_surrenders(user_id: int):
    user_session = get_existing_user_session(user_id)
    user_session.game_over(is_user_winner=False)


def game_over_user_wins(user_id):
    user_session = get_existing_user_session(user_id)
    user_session.game_over(is_user_winner=True)


def game_over_ai_wins(user_id):
    user_session = get_existing_user_session(user_id)
    user_session.game_over(is_user_winner=False)


def get_users_online(user_id: int) -> tuple[list[str], int]:
    user_index = -1
    i = 0

    def check_if_online_and_count(user_session: UserSession):
        nonlocal i
        nonlocal user_index
        if user_session.is_online:
            if user_session.user_id == user_id:
                user_index = i
            i += 1
            return True
        return False

    user_names_lst = [u.user_name for u in users.values()
                      if check_if_online_and_count(u)]
    return user_names_lst, user_index


def get_top_gamers(n, user_id) -> list[tuple[str, int, int, int, bool]]:
    sorted_users = sorted(list(users.values()),
                          key=lambda us: (us.score.total, us.score.wins))
    top_users = itertools.islice(sorted_users, n)
    top_lst = list(map(lambda us:
                       (us.user_name, us.score.total, us.score.wins,
                        us.score.losses, us.user_id == user_id),
                       top_users))
    return top_lst


def reset_interaction_state(user_session: UserSession):
    user_session.interaction_state = InteractionState.UNSPECIFIED


def set_new_candies_per_turn(user_session: UserSession, new_value: int) -> bool:
    """Изменяет параметр игры 'максимальное количество конфет за ход',
    Возвращает True, если пришлось также изменить параметр 'общего количества конфет',
    для соответствия новому значению конфет за ход.
    В противном случае возвращает False.
    """
    assert new_value >= common.MIN_ALLOWED_CANDIES_PER_TURN, 'Error: Unacceptable candies per turn new value.'
    assert user_session.interaction_state == InteractionState.SET_CANDIES_PER_TURN, 'Error: Unacceptable iteraction state.'
    game_settings = user_session.game_settings
    user_session.set_candies_per_turn(new_value)
    min_candies_total = new_value*5
    if game_settings.candies_total < min_candies_total:
        user_session.set_candies_total(min_candies_total)
        return True
    return False


def set_new_candies_total(user_session: UserSession, new_value: int) -> bool:
    """Изменяет параметр игры 'исходное общее количество конфет за ход',
    Возвращает True, если пришлось также изменить параметр 'макс. количества конфет за ход',
    для соответствия новому значению иисходного количества конфет.
    В противном случае возвращает False.
    """
    assert new_value >= common.MIN_ALLOWED_CANDIES_TOTAL, 'Error: Unacceptable candies total new value.'
    assert user_session.interaction_state == InteractionState.SET_CANDIES_TOTAL, 'Error: Unacceptable iteraction state.'
    game_settings = user_session.game_settings
    user_session.set_candies_total(new_value)
    max_candies_per_turn = new_value//5
    if game_settings.candies_per_turn > max_candies_per_turn:
        user_session.set_candies_per_turn(max_candies_per_turn)
        return True
    return False


def set_new_game_difficulty(user_session: UserSession, new_value: DifficultyLevel):
    user_session.set_difficulty(new_value)


def check_if_winner(user_id) -> bool:
    user_session = get_existing_user_session(user_id)
    game_settings = user_session.game_settings
    return user_session.game_candies_left <= game_settings.candies_per_turn


def __get_candies_to_take_optimum(candies_total, candies_per_turn):
    optimum = candies_total % (candies_per_turn + 1)
    if optimum == 0:
        return None
    return optimum


def do_ai_turn(user_id) -> tuple[int, int]:
    user_session = get_existing_user_session(user_id)
    assert user_session.interaction_state == InteractionState.GAME_AI_TURN, 'Error: Unacceptable iteraction state.'
    game_settings = user_session.game_settings
    assert user_session.game_candies_left > game_settings.candies_per_turn, 'Error: Checking for winner must be performed before this mtod call.'

    if game_settings.difficulty == DifficultyLevel.EASY:
        candies_to_take = random.randint(1, game_settings.candies_per_turn)
    else:
        candies_to_take = __get_candies_to_take_optimum(
            user_session.game_candies_left, game_settings.candies_per_turn)
        if candies_to_take is None:
            candies_to_take = random.randint(1, game_settings.candies_per_turn)

    user_session.withdraw_candies(candies_to_take)
    user_session.interaction_state = InteractionState.GAME_USER_TURN
    return candies_to_take, user_session.game_candies_left


def do_user_turn(user_id: int, candies_to_take: int) -> tuple[int, int]:
    user_session = get_existing_user_session(user_id)
    assert user_session.interaction_state == InteractionState.GAME_USER_TURN, 'Error: Unacceptable iteraction state.'
    game_settings = user_session.game_settings
    assert user_session.game_candies_left > game_settings.candies_per_turn, 'Error: Checking for winner must be performed before this mtod call.'
    assert candies_to_take <= game_settings.candies_per_turn, 'Error: Unacceptable candies_to_take value.'

    user_session.withdraw_candies(candies_to_take)
    user_session.interaction_state = InteractionState.GAME_AI_TURN
    return candies_to_take, user_session.game_candies_left
