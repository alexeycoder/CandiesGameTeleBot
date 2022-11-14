import asyncio
import random

from aiogram import types

import common
import logger
import model
import view
from bot import bot
from entities.difficulty_level import DifficultyLevel
from entities.interaction_state import InteractionState
from entities.user_session import UserSession

# shared entities:

ikb_change_game_settings = types.InlineKeyboardMarkup(row_width=1)
ikb_change_game_settings.add(
    types.InlineKeyboardButton(
        view.BTN_TXT_GAME_SET_DIFFICULTY, callback_data=common.CALLBACK_NAME_DIFFICULTY),
    types.InlineKeyboardButton(
        view.BTN_TXT_GAME_SET_PER_TURN, callback_data=common.CALLBACK_NAME_CANDIES_PER_TURN),
    types.InlineKeyboardButton(
        view.BTN_TXT_GAME_SET_TOTAL, callback_data=common.CALLBACK_NAME_CANDIES_TOTAL)
)

ikb_difficulties = types.InlineKeyboardMarkup(row_width=2)
ikb_difficulties.add(
    types.InlineKeyboardButton(
        common.DIFFICULTY_EASY_TXT, callback_data=common.CALLBACK_NAME_DIFFICULTY_EASY),
    types.InlineKeyboardButton(
        common.DIFFICULTY_HARD_TXT, callback_data=common.CALLBACK_NAME_DIFFICULTY_HARD)
)


# helper methods:

async def __emulate_typing(message: types.Message, cycles: int = 2, seconds: float = 3):
    typings = view.TYPINGS
    count = len(typings) - 2
    pause = seconds/(count*cycles)

    typings_iter = iter(typings)
    answer = await message.answer(''.join(next(typings_iter)))
    await message.answer_chat_action(types.ChatActions.TYPING)

    for _ in range(cycles):
        for typing in typings_iter:
            await asyncio.sleep(pause)
            answer = await answer.edit_text(''.join(typing))
            await message.answer_chat_action(types.ChatActions.TYPING)
        typings_iter = iter(typings)
        next(typings_iter)
        next(typings_iter)

    await asyncio.sleep(pause)
    return answer


async def __handle_new_user_if_necessary(message: types.Message, callback: types.CallbackQuery = None) -> tuple[UserSession, bool]:
    """Возвращает кортеж из UserSession для текущего собеседника, и bool состояния.

    Состояние = False когда собеседник не новый и сессия с ним всё-ещё активна.

    Состояние = True, если обеседник новый или давно отсутствовал.
    В таком случае может быть необходимо прервать последующую обработку команды."""

    user = message.from_user if callback is None else callback.from_user
    if user.is_bot:
        return None, True

    if model.is_new_user(user.id):
        await start(message, first_time=True)
        return model.get_existing_user_session(user.id), True
    else:
        need_refresh_welcome = model.user_been_away_too_long(user.id)
        us = model.get_existing_user_session(user.id)
        us.update_last_activity()
        if need_refresh_welcome:
            if model.is_user_playing(us.interaction_state):
                await back_to_game(message)
            else:
                await start(message, False)
            return us, True

        return us, False


async def __handle_hacker(message: types.Message):
    logger.log(message)
    await message.reply(view.TXT_ANGRY_EXCLAMATION)


# handlers:

async def start(message: types.Message, first_time=True):
    logger.log(message)
    user = message.from_user
    if user.is_bot:
        return

    if first_time:
        # re-check, на случай если вызвано командой /start
        if model.is_new_user(user.id):
            model.add_new_user(user.id, user.full_name)
        else:
            first_time = False

    if first_time:
        try:
            await bot.send_sticker(message.chat.id, sticker=view.get_welcome_sticker())
        except Exception:
            pass

    await bot.send_message(message.chat.id, view.get_welcome_html(user.first_name, first_time), parse_mode='html')


async def back_to_game(message: types.Message):
    logger.log(message)
    await message.answer(view.get_back_to_game_view_txt(message.from_user.first_name))
    await prompt_user_turn(message)


async def menu(message: types.Message):
    logger.log(message)
    await message.answer(text=view.get_menu_view_html(), parse_mode='html')


async def rules(message: types.Message):
    logger.log(message)
    us, _ = await __handle_new_user_if_necessary(message)

    game_settings = us.game_settings

    view_html = view.get_rules_view_html(
        game_settings.candies_total,
        game_settings.candies_per_turn,
        game_settings.difficulty.value
    )

    ikb = ikb_change_game_settings
    if model.is_user_playing(us.interaction_state):
        ikb = None
        view_html += '\n' + view.HINT_TXT_GAME_SETTINGS_DISCARD

    await message.answer(text=view_html, parse_mode='html', reply_markup=ikb)


async def settings(message: types.Message):
    logger.log(message)
    us, _ = await __handle_new_user_if_necessary(message)

    game_settings = us.game_settings

    view_html = view.get_game_settings_view_html(
        game_settings.candies_total,
        game_settings.candies_per_turn,
        game_settings.difficulty.value
    )

    ikb = ikb_change_game_settings
    if model.is_user_playing(us.interaction_state):
        ikb = None
        view_html += '\n' + view.HINT_TXT_GAME_SETTINGS_DISCARD

    await message.answer(text=view_html, parse_mode='html', reply_markup=ikb)


async def prompt_change_game_settings(callback: types.CallbackQuery):
    logger.log(callback.message)
    us, abort = await __handle_new_user_if_necessary(callback.message, callback)
    if abort or us is None:
        return

    if model.is_user_playing(us.interaction_state):
        await callback.answer(view.HINT_TXT_GAME_SETTINGS_DISCARD)
        return

    await callback.answer(view.HINT_TXT_GAME_SETTINGS)

    current_value_str = None
    default_value_str = None
    answer_view = None

    game_settings = us.game_settings
    message = callback.message
    match callback.data:
        case common.CALLBACK_NAME_DIFFICULTY:
            us.interaction_state = InteractionState.SET_DIFFICULTY
            # current_value_str = gs.difficulty.value
            # default_value_str = common.DIFFICUTLY_DEFAULT
            answer_view = view.PROMPT_TXT_GAME_SET_DIFFICULTY
            await message.answer(answer_view, reply_markup=ikb_difficulties)
            return

        case common.CALLBACK_NAME_CANDIES_PER_TURN:
            us.interaction_state = InteractionState.SET_CANDIES_PER_TURN
            current_value_str = str(game_settings.candies_per_turn)
            default_value_str = str(common.CANDIES_PER_TURN_DEFAULT)
            answer_view = view.PROMPT_TXT_GAME_SET_PER_TURN

        case common.CALLBACK_NAME_CANDIES_TOTAL:
            us.interaction_state = InteractionState.SET_CANDIES_TOTAL
            current_value_str = str(game_settings.candies_total)
            default_value_str = str(common.CANDIES_TOTAL_DEFAULT)
            answer_view = view.PROMPT_TXT_GAME_SET_TOTAL

        case _:
            await __handle_hacker(message)
            return

    ikb_alt_options = types.InlineKeyboardMarkup(row_width=1)
    ikb_alt_options.add(types.InlineKeyboardButton(
        view.get_btn_leave_current_value_txt(current_value_str), callback_data=common.CALLBACK_NAME_LEAVE_CURRENT)
    )
    if current_value_str != default_value_str:
        ikb_alt_options.add(types.InlineKeyboardButton(
            view.get_btn_to_default_value_txt(default_value_str), callback_data=common.CALLBACK_NAME_TO_DEFAULT)
        )
    await message.answer(answer_view, reply_markup=ikb_alt_options)


async def game_settings_set_difficulty(callback: types.CallbackQuery):
    logger.log(callback.message)
    us, abort = await __handle_new_user_if_necessary(callback.message, callback)
    if abort or us is None:
        return

    if model.is_user_playing(us.interaction_state):
        await callback.answer(view.HINT_TXT_GAME_SETTINGS_DISCARD)
        return

    await callback.answer(view.HINT_TXT_GAME_SETTINGS_OKAY)

    choice = callback.data
    difficulty = None
    if choice == common.CALLBACK_NAME_DIFFICULTY_EASY:
        difficulty = DifficultyLevel.EASY
    elif choice == common.CALLBACK_NAME_DIFFICULTY_HARD:
        difficulty = DifficultyLevel.HARD

    if difficulty is None:
        return

    model.set_new_game_difficulty(us, difficulty)
    # await callback.message.answer(view.get_game_difficulty_set_confirmation_html(difficulty.value), parse_mode='html')
    message = callback.message
    await message.edit_text(
        message.text + '\n\n' +
        view.get_game_difficulty_set_confirmation_html(difficulty.value),
        parse_mode='html')


async def game_settings_reset(callback: types.CallbackQuery):
    logger.log(callback.message)
    us, abort = await __handle_new_user_if_necessary(callback.message, callback)
    if abort or us is None:
        return

    game_settings = us.game_settings

    if model.is_user_playing(us.interaction_state):
        await callback.answer(view.HINT_TXT_GAME_SETTINGS_DISCARD)
        return

    await callback.answer(view.HINT_TXT_GAME_SETTINGS_OKAY)

    value_set_info = None

    message = callback.message
    match callback.data:
        case common.CALLBACK_NAME_LEAVE_CURRENT:
            if us.interaction_state in [InteractionState.SET_CANDIES_PER_TURN, InteractionState.SET_CANDIES_TOTAL]:
                us.interaction_state = InteractionState.UNSPECIFIED
                value_set_info = view.HINT_TXT_GAME_SETTINGS_VALUE_LEFT

        case common.CALLBACK_NAME_TO_DEFAULT:

            if us.interaction_state == InteractionState.SET_CANDIES_PER_TURN:
                us.interaction_state = InteractionState.UNSPECIFIED
                value_set_info = view.HINT_TXT_GAME_SETTINGS_VALUE_RESET
                game_settings.candies_per_turn = common.CANDIES_PER_TURN_DEFAULT

            elif us.interaction_state == InteractionState.SET_CANDIES_TOTAL:
                us.interaction_state = InteractionState.UNSPECIFIED
                value_set_info = view.HINT_TXT_GAME_SETTINGS_VALUE_RESET
                game_settings.candies_total = common.CANDIES_TOTAL_DEFAULT

        case _:
            await __handle_hacker(message)
            return

    if value_set_info:
        await message.edit_text(message.text + '\n\n' + value_set_info)


async def game_settings_candies_per_turn_set(message: types.Message, us: UserSession, candies_per_turn):
    logger.log(message)
    assert us.interaction_state == InteractionState.SET_CANDIES_PER_TURN, 'Unacceptable interaction state'

    if candies_per_turn < common.MIN_ALLOWED_CANDIES_PER_TURN:
        await message.answer(view.TXT_UNACCEPTABLE_CANDIES_PER_TURN)
        return

    second_param_adjusted = model.set_new_candies_per_turn(
        us, candies_per_turn)

    gs = us.game_settings
    await message.answer(view.get_candies_per_turn_set_confirmation_html(
        gs.candies_per_turn, gs.candies_total, second_param_adjusted), parse_mode='html')

    model.reset_interaction_state(us)


async def game_settings_candies_total_set(message: types.Message, us: UserSession, candies_total):
    logger.log(message)
    assert us.interaction_state == InteractionState.SET_CANDIES_TOTAL, 'Unacceptable interaction state'

    if candies_total < common.MIN_ALLOWED_CANDIES_TOTAL:
        await message.answer(view.TXT_UNACCEPTABLE_CANDIES_TOTAL)
        return

    second_param_adjusted = model.set_new_candies_total(us, candies_total)

    gs = us.game_settings
    await message.answer(view.get_candies_total_set_confirmation_html(
        gs.candies_total, gs.candies_per_turn, second_param_adjusted),
        parse_mode='html')

    model.reset_interaction_state(us)


# async def game_settings_difficulty_set(message: types.Message, us: UserSession, difficulty_str):
#     if difficulty_str in [DifficultyLevel.EASY.value, DifficultyLevel.HARD.value]:
#         model.set_new_game_difficulty(us, DifficultyLevel(difficulty_str))
#         await message.answer(view.get_game_difficulty_set_confirmation_html(difficulty_str), parse_mode='html')
#     else:
#         await __handle_hacker(message)


async def play(message: types.Message):
    logger.log(message)
    us, abort = await __handle_new_user_if_necessary(message)
    if abort:
        return

    if model.is_user_playing(us.interaction_state):
        await message.reply(view.TXT_WARN_ALREADY_IN_GAME)
        return

    whose_turn = random.choice(
        [InteractionState.GAME_AI_TURN, InteractionState.GAME_USER_TURN])
    us.new_game(whose_turn)

    await message.answer(view.HTML_THE_GAME_EXCLAMATION, parse_mode='html')
    await message.answer(view.TXT_TOSS_WHOSE_TURN)
    answer = await __emulate_typing(message, 1, 3)
    if whose_turn == InteractionState.GAME_USER_TURN:
        await answer.edit_text(view.TXT_TOSS_USER_FIRST)
        await prompt_user_turn(message)
    else:
        await answer.edit_text(view.TXT_TOSS_AI_FIRST)
        await ai_turn(message)


async def ai_turn(message: types.Message):
    logger.log(message)
    us, _ = await __handle_new_user_if_necessary(message)

    if us.interaction_state != InteractionState.GAME_AI_TURN:
        logger.log(
            message, f'ODD BEHAVIOR: user {us.user_id} got wrong interaction state {us.interaction_state} in {ai_turn.__name__}!')
        return

    if model.check_if_winner(us.user_id):
        await congratulate_ai(message, us.game_candies_left)
        model.game_over_ai_wins(us.user_id)
        return

    taken, left = model.do_ai_turn(us.user_id)
    answer = await __emulate_typing(message, 1, 4)
    await answer.edit_text(view.get_ai_turn_comment_html(taken, left), parse_mode='html')

    await prompt_user_turn(message)


async def prompt_user_turn(message: types.Message):
    logger.log(message)
    us, abort = await __handle_new_user_if_necessary(message)
    if abort:
        return

    assert us.interaction_state == InteractionState.GAME_USER_TURN, 'Unacceptable interaction state'

    if model.check_if_winner(us.user_id):
        await congratulate_user(message, us.game_candies_left)
        model.game_over_user_wins(us.user_id)
        return

    game_settings = us.game_settings
    await message.answer(view.get_user_turn_prompt_txt(game_settings.candies_per_turn))


async def user_turn_wrong_answer(message: types.Message, us: UserSession):
    logger.log(message)
    us, abort = await __handle_new_user_if_necessary(message)
    if abort:
        return

    if us.interaction_state != InteractionState.GAME_USER_TURN:
        return

    await message.reply(view.TXT_USER_TURN_WRONG_DATA)


async def user_turn(message: types.Message, us: UserSession, candies_to_take):
    logger.log(message)
    assert us.interaction_state == InteractionState.GAME_USER_TURN, 'Unacceptable interaction state'

    game_settings = us.game_settings

    if candies_to_take == 0:
        await message.reply(view.TXT_USER_TURN_TOO_LOW)
        return
    elif candies_to_take > game_settings.candies_per_turn:
        await message.reply(view.TXT_USER_TURN_TOO_MANY.format(game_settings.candies_per_turn))
        return

    taken, left = model.do_user_turn(us.user_id, candies_to_take)

    await message.reply(view.get_user_turn_comment_html(taken, left), parse_mode='html')
    await ai_turn(message)


async def congratulate_user(message: types.Message, candies_left):
    logger.log(message)
    await message.answer(view.get_user_congratulations(candies_left), parse_mode='html')
    await message.answer(view.TXT_LETS_PLAY_AGAIN)


async def congratulate_ai(message: types.Message, candies_left):
    logger.log(message)
    await message.answer(view.get_ai_congratulations(candies_left), parse_mode='html')
    await message.answer(view.TXT_LETS_PLAY_AGAIN)


async def who(message: types.Message):
    logger.log(message)
    us, _ = await __handle_new_user_if_necessary(message)

    names_lst, user_index = model.get_users_online(us.user_id)
    await message.answer(view.get_users_online_view_html(names_lst, user_index), parse_mode='html')


async def top(message: types.Message):
    logger.log(message)
    us, _ = await __handle_new_user_if_necessary(message)

    top_lst = model.get_top_gamers(common.TOP_GAMERS_NUM, us.user_id)
    await message.answer(view.get_top_gamers_view_html(top_lst), parse_mode='html')


async def score(message: types.Message):
    logger.log(message)
    us, _ = await __handle_new_user_if_necessary(message)

    us = model.get_existing_user_session(us.user_id)
    await message.answer(view.get_user_score_view_html(us.score.total, us.score.wins, us.score.losses), parse_mode='html')


async def surrender(message: types.Message):
    logger.log(message)
    us, _ = await __handle_new_user_if_necessary(message)

    if not model.is_user_playing(us.interaction_state):
        await message.reply(view.TXT_WARN_NOT_IN_GAME)
        return

    model.user_surrenders(us.user_id)

    await message.answer(view.TXT_SURRENDER_COMMENT
                         + '\n\n' +
                         view.get_user_score_view_html(
                             us.score.total, us.score.wins, us.score.losses)
                         + '\n\n' + view.TXT_LETS_PLAY_AGAIN,
                         parse_mode='html')


async def route_numeric_data(message: types.Message):
    logger.log(message)
    us, abort = await __handle_new_user_if_necessary(message)
    if abort:
        return

    value = int(message.text)

    match us.interaction_state:
        case InteractionState.GAME_USER_TURN:
            await user_turn(message, us, value)
        case InteractionState.SET_CANDIES_PER_TURN:
            await game_settings_candies_per_turn_set(message, us, value)
        case InteractionState.SET_CANDIES_TOTAL:
            await game_settings_candies_total_set(message, us, value)


async def route_nonnumeric_data(message: types.Message):
    logger.log(message)
    us, abort = await __handle_new_user_if_necessary(message)
    if abort:
        return

    value_str = message.text

    match us.interaction_state:
        case InteractionState.GAME_USER_TURN:
            await user_turn_wrong_answer(message, us)
        case InteractionState.SET_CANDIES_PER_TURN:
            await message.reply(view.TXT_ERR_NAN)
        case InteractionState.SET_CANDIES_TOTAL:
            await message.reply(view.TXT_ERR_NAN)
        # case InteractionState.SET_DIFFICULTY:
        #     await game_settings_difficulty_set(message, us, value_str)
