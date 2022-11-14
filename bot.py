from sys import stderr

import aiogram

import aux
from common import TOKEN_FILE_PATH

token, err = aux.read_token(TOKEN_FILE_PATH)
if err:
    print(err, file=stderr)
    exit(-1)

bot = aiogram.Bot(token)
dp = aiogram.Dispatcher(bot)
