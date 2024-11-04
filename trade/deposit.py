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
    max_deposit = int((bank_size - my_bank) / coefficient)
    max_deposit = 0 if max_deposit < 0 else max_deposit

    if value is None:  # вывод справки по вкладу
        balance = int(get_from_db("user", "balance", user_id))

        bot.reply_to(message,
                     "Чтобы положить лисокойны в банк введите:\n"
                     "`положить `{кол-во}\n\n"
                     "Ваш баланс " + f"{balance} лисокойн{get_name_coin(balance)}",
                     parse_mode='markdown')
    elif value.isdigit() and int(value) > 0:  # проверка, что снятие число
        value = int(value)

        if balance < value:  # проверка, что вклад меньше баланса
            bot.reply_to(message,
                         f"Недостаточно лисокойнов\n"
                         f"Вы можете положить ещё `{max_deposit}` лисокойн{get_name_coin(max_deposit)}",
                         parse_mode='markdown')
        elif my_bank + int(value * coefficient) > bank_size:  # проверка, что банк не переполнится
            bot.reply_to(message,
                         f"Сумма вклада слишком велика\n"
                         f"Вы можете положить ещё `{max_deposit}` лисокойн{get_name_coin(max_deposit)}",
                         parse_mode='markdown')
        else:
            value_minus = value - int(value * coefficient)
            value = int(value * coefficient)  # комиссия 20% для не вип и 1% для вип пользователей

            if bank_size - value - my_bank == 1:
                value += 1

                set_in_db("trade", "bank", f"{bank_size}", user_id)
                set_in_db("user", "balance", f"{balance - value - value_minus}", user_id)
                bot.reply_to(message,
                             f"Успешно вложено {value} лисокойн{get_name_coin(value)}\n"
                             f"Комиссия составила {int(value * 0.01) + 1 if isVip != 0 else int(value * 0.2) + 1}")
            elif bank_size - value - my_bank <= 0:
                bot.reply_to(message,
                             text="В банке больше нет места для вклада")
            else:
                set_in_db("trade", "bank", f"{my_bank + value}", user_id)
                bot.reply_to(message,
                             f"Успешно вложено {value} лисокойн{get_name_coin(value)}\n"
                             f"Комиссия составила {int(value * 0.01) + 1 if isVip != 0 else int(value * 0.2) + 1}")
                set_in_db("user", "balance", f"{balance - value - value_minus}", user_id)

    elif value.lower().replace("ё", "е") in {'все', 'all'} and balance != 0:
        if max_deposit == 0:
            bot.reply_to(message,
                         text="В банке больше нет места для вклада")
        else:
            if balance > max_deposit:
                value = max_deposit
            else:
                value = balance

            value_minus = value - int(value * coefficient)
            value = int(value * coefficient)  # комиссия 20% для не вип и 1% для вип пользователей

            if bank_size - value - my_bank == 1:
                value += 1

                set_in_db("trade", "bank", f"{bank_size}", user_id)
                set_in_db("user", "balance", f"{balance - value - value_minus}", user_id)
                bot.reply_to(message,
                             f"Успешно вложено {value} лисокойн{get_name_coin(value)}\n"
                             f"Комиссия составила {value_minus} лисокойн{get_name_coin(value_minus)}")
            else:
                set_in_db("trade", "bank", f"{my_bank + value}", user_id)
                set_in_db("user", "balance", f"{balance - value - value_minus}", user_id)
                bot.reply_to(message,
                             f"Успешно вложено {value} лисокойн{get_name_coin(value)}\n"
                             f"Комиссия составила {value_minus} лисокойн{get_name_coin(value_minus)}")

    else:
        bot.reply_to(message,
                     f"Вложение должно быть числом, причём больше нуля")
