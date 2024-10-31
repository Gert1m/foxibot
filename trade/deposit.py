from telebot import TeleBot
from db import *
from bot_token import token

bot = TeleBot(token)  # token = "token from botFather"


async def deposit(message, value=None):
    user_id = message.from_user.id
    balance = int(get_from_db("user", "balance", user_id))
    my_bank = int(get_from_db("trade", "bank", user_id))
    isVip = int(get_from_db("user", "isVip", user_id))
    bank_size = 5000
    coefficient = 0.99 if isVip != 0 else 0.8

    if value is None:  # вывод справки по вкладу
        balance = int(get_from_db("user", "balance", user_id))

        bot.reply_to(message,
                     "Чтобы положить лисокойны в банк введите:\n"
                     "`положить `{кол-во}\n\n"
                     "Ваш баланс " + f"{balance} лисокойн{get_name_coin(balance)}",
                     parse_mode='markdown')
    elif value.isdigit():  # проверка, что снятие число
        value = int(value)
        max_deposit = int((bank_size - my_bank) / coefficient)

        if balance <= value:  # проверка, что вклад меньше баланса
            bot.reply_to(message,
                         f"Недостаточно лисокойнов\n"
                         f"Вы можете положить ещё `{max_deposit}` лисокойн{get_name_coin(max_deposit)}",
                         parse_mode='markdown')
        elif my_bank + int(value * coefficient) >= bank_size:  # проверка, что банк не переполнится
            bot.reply_to(message,
                         f"Сумма вклада слишком велика\n"
                         f"Вы можете положить ещё `{max_deposit}` лисокойн{get_name_coin(max_deposit)}",
                         parse_mode='markdown')
        else:
            value = int(value * 0.99) if isVip != 0 else int(
                value * 0.8)  # комиссия 20% для не вип и 1% для вип пользователей
            if bank_size - value - my_bank <= 1:
                set_in_db("trade", "bank", f"{bank_size}", user_id)
            else:
                set_in_db("trade", "bank", f"{my_bank + value}", user_id)

            set_in_db("user", "balance", f"{balance - value}", user_id)

            if bank_size - value - my_bank <= 1:
                bot.reply_to(message,
                             f"Успешно вложено {value + 1} лисокойн{get_name_coin(value + 1)}\n"
                             f"Комиссия составила {"1%" if isVip != 0 else "20%"}")
            else:
                bot.reply_to(message,
                             f"Успешно вложено {value} лисокойн{get_name_coin(value)}\n"
                             f"Комиссия составила {"1%" if isVip != 0 else "20%"}")

    elif value.lower().replace("ё", "е") in {'все', 'all'} and balance != 0:
        value = int(balance * 0.99) if isVip != 0 else int(
            balance * 0.8)  # комиссия 20% для не вип и 1% для вип пользователей

        set_in_db("user", "balance", f"{balance - balance}", user_id)
        set_in_db("trade", "bank", f"{my_bank + value}", user_id)

        if bank_size - value - my_bank <= 1:
            bot.reply_to(message,
                         f"Успешно вложено {value + 1} лисокойн{get_name_coin(value + 1)}\n"
                         f"Комиссия составила {"1%" if isVip != 0 else "20%"}")
        else:
            bot.reply_to(message,
                         f"Успешно вложено {value} лисокойн{get_name_coin(value)}\n"
                         f"Комиссия составила {"1%" if isVip != 0 else "20%"}")

    else:
        bot.reply_to(message,
                     f"Вложение должно быть числом")
