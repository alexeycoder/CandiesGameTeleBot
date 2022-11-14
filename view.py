import random

from common import (CMD_MENU, CMD_PLAY, CMD_PREFIX, CMD_RULES, CMD_SCORE,
                    CMD_SETTINGS, CMD_SURRENDER, CMD_TOP, CMD_WHO,
                    MIN_ALLOWED_CANDIES_PER_TURN, MIN_ALLOWED_CANDIES_TOTAL,
                    MAIN_STICKER_TOKEN)

HTML_MENU = (
    '<em>Доступные команды:</em>'
    f'\n{CMD_PREFIX}{CMD_MENU} - данное меню'
    f'\n{CMD_PREFIX}{CMD_PLAY} - начать игру'
    f'\n{CMD_PREFIX}{CMD_RULES} - правила игры'
    f'\n{CMD_PREFIX}{CMD_SETTINGS} - параметры'
    f'\n{CMD_PREFIX}{CMD_SURRENDER} - сдаться'
    f'\n{CMD_PREFIX}{CMD_SCORE} - твой игровой счёт'
    f'\n{CMD_PREFIX}{CMD_WHO} - игроки онлайн'
    f'\n{CMD_PREFIX}{CMD_TOP} - топ-10 игроков'
)

BTN_TXT_GAME_SET_PER_TURN = 'Изменить максимум конфет за ход'
BTN_TXT_GAME_SET_TOTAL = 'Изменить исходное количество конфет'
BTN_TXT_GAME_SET_DIFFICULTY = 'Задать уровень сложности'

PROMPT_TXT_GAME_SET_PER_TURN = ('Задайте в ответе максимальное количество конфет,'
                                f' которое можно взять за ход (не менее {MIN_ALLOWED_CANDIES_PER_TURN}),'
                                ' либо выберите одну доступных опций:')
PROMPT_TXT_GAME_SET_TOTAL = ('Задайте в ответе исходное общее количество конфет'
                             f' (но не менее {MIN_ALLOWED_CANDIES_TOTAL}), либо выберите одну доступных опций:')
PROMPT_TXT_GAME_SET_DIFFICULTY = 'Выберите уровень сложности:'

BTN_TXT_GAME_SET_LEAVE_VALUE = 'Оставить текущее значение ({})'
BTN_TXT_GAME_SET_TO_DEFAULT = 'Установить значение по умолчанию ({})'
HINT_TXT_GAME_SETTINGS = 'Редактирование параметров игры'
HINT_TXT_GAME_SETTINGS_DISCARD = 'В процессе игры изменение параметров не допускается.'
HINT_TXT_GAME_SETTINGS_OKAY = 'Okay!'
HINT_TXT_GAME_SETTINGS_DONE = 'Сделано!'
HINT_TXT_GAME_SETTINGS_INV = 'Нельзя!'
HINT_TXT_GAME_SETTINGS_VALUE_LEFT = 'Оставлено без изменений.'
HINT_TXT_GAME_SETTINGS_VALUE_RESET = 'Сброшено к значению по умолчанию.'
TXT_TRY_AGAIN = 'Попробуй задать более подходящее значение:'
TXT_UNACCEPTABLE_CANDIES_PER_TURN = ('Максимальное количество конфет, которое можно взять за ход,'
                                     f' должно быть не меньше {MIN_ALLOWED_CANDIES_PER_TURN}'
                                     f'\n{TXT_TRY_AGAIN}')
TXT_UNACCEPTABLE_CANDIES_TOTAL = ('Исходное общее количество конфет'
                                  f' должно быть не меньше {MIN_ALLOWED_CANDIES_TOTAL}'
                                  f'\n{TXT_TRY_AGAIN}')
TXT_ERR_NAN = '\U0001F47E Попробуй лучше, дружочек. Нужны циферки, целое число:'

HTML_RULES = """<em>Правила игры <b>\"Отбери все конфетки\"</b></em>:

На столе лежит <b>{}</b> конфет.
Играют два игрока делая ход друг после друга.
Чей первый ход \u2014 определяется жеребьёвкой.
За один ход можно забрать не более чем <b>{}</b> конфет, но не менее одной.
Выигрывает тот, кто последним забирает оставшиеся конфеты.

Текущий уровень сложности: <b>{}</b>
Исходные параметры игры можно изменить:
"""

HTML_GAME_SETTINGS = """Исходное общее число конфет: <b>{}</b>
Максимально можно взять за ход: <b>{}</b>
Уровень сложности: <b>{}</b>
"""

HTML_USER_SCORE_SHORT = "{}:\t\U0001F93C {},\t\U0001F44D {},\t\U0001F44E {}"
HTML_USER_SCORE_FULL = ('<em>Твой текущий игровой счёт:</em>'
                        '\nВсего сыграно: <b>{}</b>,'
                        '\nиз них выиграно: <b>{}</b>,'
                        '\nпроиграно: <b>{}</b>.')

TXT_ANGRY_EXCLAMATION = 'Чо?! \U0001F47F'

TXT_WARN_ALREADY_IN_GAME = f'В процессе игры нельзя начать новую игру!\nЖелаешь сдаться? \U0001F449{CMD_PREFIX}{CMD_SURRENDER}'
TXT_WARN_NOT_IN_GAME = f'Вот те раз! Погоди сдаваться не начав игры!\nЖелаешь начать новую игру? \U0001F449{CMD_PREFIX}{CMD_PLAY}'

HTML_THE_GAME_EXCLAMATION = 'Уии! \U0001F437 \U0001F3C1 <b><em>Начинаем игру!</em></b> \U0001F3C1'
TXT_TOSS_WHOSE_TURN = 'Жеребьёвка первого хода...'
TXT_TOSS_USER_FIRST = 'Тебе достаётся первый ход! \U0001F416'
TXT_TOSS_AI_FIRST = 'Мне достаётся первый ход! Уии \U0001F437'

TXT_SURRENDER_COMMENT = ' \U0001F437 Прекрассно понимаю \u2014 ведь меня невозможно ни обыграть, ни обрыгать! \U0001F43D Хрю'

HTML_AI_TURN_COMMENT = ('<em>Мой ход</em> \U0001F416'
                        '\nИзъяла <b>{}</b> \U0001F36C, осталось <b>{}</b> \U0001F36C\U0001F36C\n')

LST_AI_TURN_COMMENTS_EXTRA = \
    ['\U0001F437 Обещаю поделиться с подружками \U0001F411\U0001F438 Хрю-хрю',
     '\U0001F437 И даже это меньше чем ты обычно съедаешь! Хрю \U0001F607',
     '\U0001F43D Ты хоть понимаешь какую я тебе услугу оказываю!? Тебе эти конфеты ни к чему! Хрю \U0001F437',
     '\U0001F437 Из конфет я варю прекрассное варенье, копытца оближешь!  \U0001F36C\U0001F63B',
     '\U0001F43D Мой пятачок приспособлем для конфет и никогда не слипнется. А вот у тебя проблемы! \U0001F636 Хрю',
     '\U0001F437 Давай ты отдашь мне все конфетки, и я не буду делать сюрприз тебе под порогом \U0001F423']

TXT_USER_TURN_PROMPT = ('Тебе ходить. Сколько конфеток возьмёшь?'
                        '\n(Напоминаю, можно взять не более {} конфет. '
                        f'А ещё ты всегда можешь сдаться? \U0001F449{CMD_PREFIX}{CMD_SURRENDER})')

HTML_USER_TURN_COMMENT = ('<em>Твой ход</em> \U0001F61C'
                          '\nСтырено <b>{}</b> \U0001F36C, осталось <b>{}</b> \U0001F36C\U0001F36C\n')

LST_USER_TURN_COMMENTS_EXTRA = \
    ['\U0001F60B Бери не стесняйся, в конфетах все самые важные витамины и микроэлементы! Хрю',
     '\U0001F910 А што же так скромно? Не поразил ли тебя вирус диеты? Куда я дела градусник...',
     '\U0001F60B У тебя такие аппетиты, што я начинаю заподазривать кое-што \U0001F930',
     '\U0001F924 Если выиграешь, ты же обещаешь устроить конфетную вечеринку для нас для всех, а? Хрю',
     '\U0001F4FF Из конфеток можно сделать съедобные бусы. Роскошная вещь. Подаришь мне такие? Хрю',
     '\U0001F60C Ой, а ты вкурсе что сегодня всемирный день свинок? Понимаешь намёк? \U0001F607']

TXT_USER_TURN_WRONG_DATA = ('\U0001F9D0 Ты же ещё помнишь как выглядят циферки? \U0001F377'
                            ' Такие закорючки... Чтобы сделать свой ход надо отправить целое число!'
                            '\nПопробуй ещё раз:')
TXT_USER_TURN_TOO_LOW = 'Как же так!? Надо взять хотя бы одну \U0001F36C'

TXT_USER_TURN_TOO_MANY = ('Это што!? \U0001F640 \"Голодающие подъехали\"... Сказано же \u2014 не более {} \U0001F36C'
                          '\nПопробуй ещё раз:')

HTML_CONGRAT_USER = ('<em><b>Победа!</b></em>'
                     '\n\U0001F640 Ой, смотри, число оставшихся конфет {} \u2014 меньше, чем можно взять за ход.'
                     '\nШтож, поздравляю с победой! \U0001F942 Нате грамоту \U0001F4C3'
                     '\nИ напоминаю про твоё обещание устроить конфетную вечеринку для нас для всех \U0001F36D Хрю')

HTML_CONGRAT_AI = ('<em><b>Конец игры!</b></em>'
                   '\n\U0001F416 Вот и пробил тот самый час.'
                   ' Число оставшихся конфет {} \u2014 меньше, чем можно взять за ход и я их забираю.'
                   '\nПобеда за мной! Ура! \U0001F37E\U0001F36C'
                   '\nВот, держи утешительный леденец \U0001F36D')

TXT_LETS_PLAY_AGAIN = f'Хочешь сыграть ещё разок? \U0001F449{CMD_PREFIX}{CMD_PLAY}\nМеню \U0001F449{CMD_PREFIX}{CMD_MENU}'


SMALL_DOT = '\u00b7'
BIG_DOT = '\u2022'
TYPINGS = ((SMALL_DOT,),
           (SMALL_DOT,)*2,
           (SMALL_DOT,)*3,
           (BIG_DOT, SMALL_DOT, SMALL_DOT),
           (SMALL_DOT, BIG_DOT, SMALL_DOT),
           (SMALL_DOT, SMALL_DOT, BIG_DOT),
           (BIG_DOT, SMALL_DOT, SMALL_DOT),
           (BIG_DOT, BIG_DOT, SMALL_DOT),
           (BIG_DOT, BIG_DOT, BIG_DOT))


def get_welcome_sticker():
    return MAIN_STICKER_TOKEN


def get_welcome_html(user_name, firts_time=False):
    view_html = f'Приветики-конфетики, {user_name}!\n'
    if not firts_time:
        view_html += 'Помнишь меня?'

    view_html += '\U0001F437 Я свинка Пеппа Конфетчица.'

    if firts_time:
        view_html += ' Приятно познакомиться. Держи копытце \U0001F91D'

    view_html += ('\nПо выходным я работаю главой маркетингового отдела Останкинского МПЗ,'
                  ' а в будни увлекаюсь игрой <b>\"Отбери все конфетки\"</b>.\n'
                  'И предлагаю тебе сыграть со мной!'
                  f'\n\nЖми \U0001F449 {CMD_PREFIX}{CMD_RULES} \U0001F448 чтобы узнать правила игры. Они очень простые.'
                  f'\n\U0001F4DC {CMD_PREFIX}{CMD_MENU} \U0001F448 меню команд')
    return view_html


def get_back_to_game_view_txt(user_name):
    return (f'Приветики-конфетики, {user_name},'
            '\nКажется у нас осталась неоконченная игра... я всё помню.')


def get_menu_view_html():
    return HTML_MENU


def get_rules_view_html(total, per_turn, difficulty_str):
    return HTML_RULES.format(total, per_turn, difficulty_str)


def get_game_settings_view_html(total, per_turn, difficulty_str):
    return HTML_GAME_SETTINGS.format(total, per_turn, difficulty_str)


def get_btn_leave_current_value_txt(value):
    return BTN_TXT_GAME_SET_LEAVE_VALUE.format(value)


def get_btn_to_default_value_txt(value):
    return BTN_TXT_GAME_SET_TO_DEFAULT.format(value)


def get_user_score_view_html(total, wins, losses):
    return HTML_USER_SCORE_FULL.format(total, wins, losses)


def get_users_online_view_html(names_lst, user_index):
    view_html = '<em>Игроки онлайн:</em>\n'

    names_lst[user_index] = f'<b>{names_lst[user_index]}</b>'

    if len(names_lst) > 0:
        view_html += '\U0001F633 '
    view_html += '\n\U0001F633 '.join(names_lst)
    view_html += '\n... <em>всё знакомые граждане... или нет(?)</em> \U0001F607'

    return view_html


def get_top_gamers_view_html(top_lst: list[tuple[str, int, int, int, bool]]):
    view_html = '<em>ТОП-10 игроков:</em>'

    for gamer in top_lst:
        name, total, wins, losses, is_user = gamer
        if is_user:
            name = f'<b>{name}</b>'
        view_html += '\n' + \
            HTML_USER_SCORE_SHORT.format(name, total, wins, losses)

    return view_html


def get_ai_turn_comment_html(candies_taken, candies_left):
    view_html = HTML_AI_TURN_COMMENT.format(candies_taken, candies_left)
    view_html += random.choice(LST_AI_TURN_COMMENTS_EXTRA)
    return view_html


def get_user_turn_prompt_txt(candies_per_turn):
    return TXT_USER_TURN_PROMPT.format(candies_per_turn)


def get_user_turn_comment_html(candies_taken, candies_left):
    view_html = HTML_USER_TURN_COMMENT.format(candies_taken, candies_left)
    view_html += random.choice(LST_USER_TURN_COMMENTS_EXTRA)
    return view_html


def get_user_congratulations(candies_left):
    return HTML_CONGRAT_USER.format(candies_left)


def get_ai_congratulations(candies_left):
    return HTML_CONGRAT_AI.format(candies_left)


def get_candies_per_turn_set_confirmation_html(per_turn: int, total: int, total_adjusted: bool):
    view_html = f'Успешно установлено новое максимальное число конфет за ход: <b>{per_turn}</b>'
    if total_adjusted:
        view_html += (f'\nТак же было скорректировано исходное общее количество конфет до <b>{total}</b>,'
                      ' поскольку прежнего количества теперь маловато (разница менее чем в 5 раз).')
    return view_html


def get_candies_total_set_confirmation_html(total: int, per_turn: int, per_turn_adjusted: bool):
    view_html = f'Успешно установлено новое исходное общее число конфет: <b>{total}</b>'
    if per_turn_adjusted:
        view_html += (f'\nТак же было скорректировано максимальное количество конфет за ход до <b>{per_turn}</b>,'
                      ' поскольку прежнее количество стало слишком велико (разница менее чем в 5 раз).')
    return view_html


def get_game_difficulty_set_confirmation_html(difficulty):
    return f'Установлен уровень сложности: <b>{difficulty}</b>'
