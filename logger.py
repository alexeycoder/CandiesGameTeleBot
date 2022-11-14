from datetime import datetime
import inspect
from sys import stderr
# from telegram import Update
import os
import ntpath
from aiogram import types

from common import LOGS_PATH, LOG_FILENAME_PFX, LOG_FILENAME_EXT

log_file = None


def get_module_name():
    return ntpath.basename(inspect.stack()[2].filename)


def get_timestamp():
    return datetime.now().strftime("%H:%M:%S")


def start_logging(console_out=True):
    global log_file
    if log_file:
        return

    if not os.path.exists(LOGS_PATH):
        os.makedirs(LOGS_PATH)

    today_date_str = datetime.now().strftime('%Y-%m-%d')
    log_file_path = f'{LOG_FILENAME_PFX}{today_date_str}.{LOG_FILENAME_EXT}'
    log_file_path = os.path.join(LOGS_PATH, log_file_path)

    try:
        log_msg = f'\n{get_timestamp()};\t{get_module_name()}\tSTART LOGGING\n'
        log_file = open(log_file_path, 'at', encoding='utf-8')
        log_file.write(log_msg)
        if console_out:
            print(log_msg)
    except OSError:
        log_file = None
        print('Ошибка: Не удалось запустить логирование!', file=stderr)


def stop_logging(console_out=True):
    global log_file
    if log_file:
        log_msg = f'\n{get_timestamp()};\t{get_module_name()}\tSTOP LOGGING\n'
        log_file.write(log_msg)
        log_file.close()
        log_file = None
        if console_out:
            print(log_msg)


def log(message: types.Message, error_msg=None, console_out=True) -> None:
    global log_file
    if log_file is None:
        return

    caller_name = inspect.stack()[1].function
    module_filename = get_module_name()
    log_data = []
    log_data.append(datetime.now().strftime("%H:%M:%S"))
    log_data.append(message.from_user.id)
    log_data.append(message.from_user.full_name)
    log_data.append(f'{module_filename}.{caller_name.upper()}')
    log_data.append(message.text)
    if error_msg:
        log_data.append('ERROR: ' + error_msg)

    log_msg = ';\t'.join(map(str, log_data))
    log_file.write(log_msg + '\n')
    log_file.flush()
    if console_out:
        print(log_msg)


def _test():
    print(datetime.now().strftime('%Y-%m-%d'))
    print('☻️'.encode('unicode_escape'))
    print('\u263b\ufe0f')
    print(get_module_name())


if __name__ == "__main__":
    _test()
