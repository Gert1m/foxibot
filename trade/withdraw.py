from telebot import TeleBot
from db import *

from bot_token import token

bot = TeleBot(token)  # token = "token from botFather"


async def withdraw(message, value=None):
    user_id = message.from_user.id
    balance = int(get_from_db("user", "balance", user_id))
    my_bank = int(get_from_db("trade", "bank", user_id))

    if value is None:  # вывод справки по снятию
        bot.reply_to(message,
                     "Чтобы забрать лисокойны с банка введите:\n`снять `{кол-во}\n\nВ вашем банке сейчас " + f"{my_bank} лисокойн{get_name_coin(my_bank)}",
                     parse_mode='markdown')
    elif value.isdigit():  # проверка, что снятие число
        value = int(value)

        if my_bank <= value:  # проверка, что снятие не больше чем банк
            bot.reply_to(message,
                         f"В банке недостаточно лисокойнов")
        else:
            set_in_db("user", "balance", f"{balance + value}", user_id)
            set_in_db("trade", "bank", f"{my_bank - value}", user_id)
            bot.reply_to(message, f"Успешно забрано {value} лисокойн{get_name_coin(value)}")
    elif value.lower().replace("ё", "е") in {'все', 'all'}:
        value = my_bank

        set_in_db("user", "balance", f"{balance + value}", user_id)
        set_in_db("trade", "bank", f"{my_bank - value}", user_id)

        bot.reply_to(message,
                     f"Успешно забрано {value} лисокойн{get_name_coin(value)}")
    else:
        bot.reply_to(message, f"Снятие должно быть числом.")
