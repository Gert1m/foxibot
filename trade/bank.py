from random import randint
from time import time
from telebot import TeleBot
from db import *
from bot_token import token

bot = TeleBot(token)  # token = "token from botFather"


async def bank(message):
    user_id = message.from_user.id
    my_bank = int(get_from_db("trade", "bank", user_id))
    isVip = int(get_from_db("user", "isVip", user_id))
    total_spent = int(get_from_db("upgrade", "total_spent", user_id))
    bank_size = 5000 + 50 * (total_spent // 1250)
    max_bank_size = bank_size * 2 if isVip != 0 else bank_size * 1.5

    if my_bank != 0:
        my_coefficient = int(float(get_from_db("trade", "coefficient", user_id)) * 100) / 100
        bot.reply_to(message,
                     f"В вашем банке `{my_bank}` лисокойн{get_name_coin(my_bank)} под {my_coefficient}% в день\n"
                     f"Макс. вклад в банк ***{bank_size // 1000 if bank_size % 1000 == 0 else bank_size / 1000} тыс. лисокойн{get_name_coin(bank_size)}\n***"
                     f"Размер банка ***{max_bank_size // 1000 if max_bank_size % 1000 == 0 else max_bank_size / 1000} тыс. лисокойн{get_name_coin(max_bank_size)}***",
                     parse_mode='markdown')
    else:
        bot.reply_to(message,
                     f"В вашем банке нет лисокойнов\n"
                     f"Макс. вклад в банк ***{bank_size // 1000 if bank_size % 1000 == 0 else bank_size / 1000} тыс. лисокойн{get_name_coin(bank_size)}\n***"
                     f"Размер банка ***{max_bank_size // 1000 if max_bank_size % 1000 == 0 else max_bank_size / 1000} тыс. лисокойн{get_name_coin(max_bank_size)}***",
                     parse_mode='markdown')


async def coefficient(message):
    bank_coefficient = float(get_from_db("trade", "coefficient", -1))
    bot.reply_to(message, f"Текущий процент в банке {bank_coefficient}%")


async def update_coefficient():
    # обновляем коэффициент раз в 2 часа
    if int(get_from_db("trade", "farm_time", -1)) <= int(time()):
        my_coefficient = float(get_from_db("trade", "coefficient", -1)) // 1

        if my_coefficient < 7:  # если коэффициент мал то
            if randint(1, 3) == 1:  # с шансом 66% его увеличиваем
                my_coefficient += -1
            else:
                my_coefficient += 1
            my_coefficient += randint(0, 99) / 100  # случайная часть после запятой 0.00-0.99
        elif my_coefficient > 14:  # если коэффициент велик
            if randint(1, 3) == 1:  # то с шансом 66% его уменьшаем
                my_coefficient += 1
            else:
                my_coefficient += -1
            my_coefficient += randint(0, 99) / 100  # случайная часть после запятой 0.00-0.99
        else:
            my_coefficient += randint(-1, 1)  # если коэффициент обычный, то с шансами 50/50 увеличиваем/уменьшаем
            my_coefficient += randint(0, 99) / 100  # случайная часть после запятой 0.00-0.99

        if my_coefficient >= 20:  # коэффициент не может быть больше 20
            my_coefficient = 20
        elif my_coefficient <= 0:  # и меньше 0
            my_coefficient = 0

        set_in_db("trade", "farm_time", f"{int(time()) + 7200}", -1)
        set_in_db("trade", "coefficient", f"{my_coefficient}", -1)
