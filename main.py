import aiogram

import bot
import handlers_registrar
import logger


def run_bot():
    handlers_registrar.register(bot.dp)
    aiogram.executor.start_polling(bot.dp, skip_updates=True)


if __name__ == '__main__':
    logger.start_logging()
    run_bot()
    logger.stop_logging()
