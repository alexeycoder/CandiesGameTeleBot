from aiogram import Dispatcher, filters, types

import commands
import common
from common import (CMD_MENU, CMD_PLAY, CMD_RULES, CMD_SCORE, CMD_SETTINGS,
                    CMD_START, CMD_SURRENDER, CMD_TOP, CMD_WHO)


def register(dp: Dispatcher):

    dp.register_message_handler(commands.start, commands=[CMD_START])
    dp.register_message_handler(commands.menu, commands=[CMD_MENU])
    dp.register_message_handler(commands.play, commands=[CMD_PLAY])
    dp.register_message_handler(commands.rules, commands=[CMD_RULES])
    dp.register_message_handler(commands.settings, commands=[CMD_SETTINGS])
    dp.register_message_handler(commands.who, commands=[CMD_WHO])
    dp.register_message_handler(commands.top, commands=[CMD_TOP])
    dp.register_message_handler(commands.surrender, commands=[CMD_SURRENDER])
    dp.register_message_handler(commands.score, commands=[CMD_SCORE])
    dp.register_message_handler(commands.route_numeric_data,
                                lambda message: message.text.isdigit())
    dp.register_message_handler(commands.route_nonnumeric_data,
                                lambda message: not message.text.isdigit())
    dp.register_callback_query_handler(commands.prompt_change_game_settings,
                                       filters.Text(
                                           (common.CALLBACK_NAME_DIFFICULTY,
                                            common.CALLBACK_NAME_CANDIES_PER_TURN,
                                            common.CALLBACK_NAME_CANDIES_TOTAL))
                                       )

    dp.register_callback_query_handler(
        commands.game_settings_reset,
        filters.Text(
            (common.CALLBACK_NAME_LEAVE_CURRENT,
             common.CALLBACK_NAME_TO_DEFAULT))
    )

    dp.register_callback_query_handler(
        commands.game_settings_set_difficulty,
        filters.Text(
            (common.CALLBACK_NAME_DIFFICULTY_EASY,
             common.CALLBACK_NAME_DIFFICULTY_HARD))
    )

    async def __try_callback_as_command(callback: types.CallbackQuery):
        data = callback.data
        if not data.startswith(common.CMD_PREFIX):
            return

        cmd_name = data[1:]
        cmd_handlers = dp.message_handlers.handlers
        if cmd_handlers is None:
            return

        for h in cmd_handlers:
            for f in h.filters:
                if isinstance(f.filter, filters.Command):
                    if cmd_name in f.filter.commands:
                        await h.handler(callback.message)
                        return

    dp.register_callback_query_handler(
        __try_callback_as_command, filters.Regexp(f'^{common.CMD_PREFIX}'))

    async def __show_sticker_token(message: types.Message):
        sticker = message.sticker
        if sticker is None:
            return
        await message.answer(message.sticker.file_id)

    dp.register_message_handler(
        __show_sticker_token, content_types=['sticker'])
