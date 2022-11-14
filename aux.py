import os

ERRTMPLT_EMPTY_FILE = 'Предупреждение: Файл \'{}\' пуст.'
ERRTMPLT_CANNOT_OPEN = '! Ошибка: Не удалось открыть файл \'{}\' для чтения!'
ERRTMPLT_CANNOT_CREATE = '! Ошибка: Не удалось создать пустой файл \'{}\'!'


def read_token(filepath) -> tuple[str, str]:
    "Возвращает кортеж ( токен , сообщение о причине, если не удалось прочесть токен )."
    if os.path.isfile(filepath):
        try:
            with open(filepath, 'rt') as file:
                data = file.read().strip()
                if len(data) == 0:
                    return (None, ERRTMPLT_EMPTY_FILE.format(filepath))
                return (data, None)
        except OSError:
            return (None, ERRTMPLT_CANNOT_OPEN.format(filepath))
    else:
        try:
            with open(filepath, 'wt') as _:
                return (None, ERRTMPLT_EMPTY_FILE.format(filepath))
        except OSError:
            pass
    return (None, ERRTMPLT_CANNOT_CREATE.format(filepath))
