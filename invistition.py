from datetime import datetime
from telebot import types

from bot_token import token
from db import *

bot = token


async def trading():
    try:
        connect = sqlite3.connect("trade.db")
        cursor = connect.cursor()
        cursor.execute("SELECT SUM(deposit) FROM trade")
        value = int(cursor.fetchone()[0])
        cursor.execute("SELECT COUNT(deposit) FROM trade")
        count = int(cursor.fetchone()[0])
        connect.close()
        coefficient = (2000 - (int(value / (25000 * count) * 100))) / 100
        if coefficient < 0:
            coefficient = 0
        in_trade_set_coefficient(-1, coefficient)
    except:
        pass


async def invistition(message):
    try:
        coefficient = in_trade_get_coefficient(-1)
        balance = in_user_get_balance(message.from_user.id)
        name_coin = get_name_coin(balance)

        inline_button = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton("Положить", callback_data="deposit"))
        bot.reply_to(message, f'''Сейчас банк принимает лисокойны под {coefficient} % в день. За раз вы можете положить не менее 100 лисокойнов и комиссия по вкладу составит 20%.
Ваш баланс: {balance} {name_coin}''', reply_markup=inline_button)
    except:
        bot.reply_to(message, "Упс.. что-то пошло не так. Попробуйте позже.")


async def claim_invistition(message):
    try:
        coefficient = in_trade_get_coefficient(message.from_user.id)
        bank = in_trade_get_deposit(message.from_user.id)
        name_coin = get_name_coin(bank)

        inline_button = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton("Снять", callback_data="withdraw"))
        bot.reply_to(message,
                     f"Сейчас в вашем банке находится {bank} {name_coin} под {coefficient}% в день. Вы желаете их забрать?",
                     reply_markup=inline_button)
    except:
        pass


async def deposit(user_id, chat_id):
    try:
        deposit_inline_buttons = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton("Отменить вклад", callback_data="cancer_deposit"))
        last_deposit = in_trade_get_deposit(user_id)
        balance = in_user_get_balance(user_id)
        username = in_user_get_username(user_id)
        if balance < 100:
            bot.send_message(chat_id, f"{username}, у вас недостаточно лисокойнов!")
        else:
            if balance > int((5000 - last_deposit) / 0.8) > 0:
                balance = int((5000 - last_deposit) / 0.8)
                bot.send_message(chat_id, f"{username}, введите сумму взноса до {balance} лисокойнов.",
                                 reply_markup=deposit_inline_buttons)
            elif int((5000 - last_deposit) / 0.8) < 0:
                bot.send_message(chat_id, f"{username}, введите сумму взноса до 0 лисокойнов.",
                                 reply_markup=deposit_inline_buttons)
            in_user_set_isDeposit(user_id, 1)
    except:
        pass


async def withdraw(user_id, chat_id):
    try:
        withdraw_inline_buttons = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton("Отменить снятие", callback_data="cancer_withdraw"))
        deposit = in_trade_get_deposit(user_id)
        username = in_user_get_username(user_id)
        if deposit > 0:
            name_coin = get_name_coin(deposit)
            bot.send_message(chat_id,
                             f"{username}, cколько лисокойнов хотите забрать из банка? На данный момент в банке хранится {deposit} {name_coin}.",
                             reply_markup=withdraw_inline_buttons)
            in_user_set_isWithdraw(user_id, 1)
        else:
            bot.send_message(chat_id, f"{username}, в банке нет лисокойнов.")
    except:
        pass


async def depositing(message, deposit):
    try:
        deposit_inline_buttons = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton("Отменить вклад", callback_data="cancer_deposit"))
        withdraw_inline_buttons = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton("Отменить снятие", callback_data="cancer_withdraw"))
        isDeposit = in_user_get_isDeposit(message.from_user.id)
        username = in_user_get_username(message.from_user.id)
        try:
            if isDeposit == 1:
                balance = in_user_get_balance(message.from_user.id)
                last_deposit = in_trade_get_deposit(message.from_user.id)
                coefficient = in_trade_get_coefficient(-1)
                isWithdraw = in_user_get_isWithdraw(message.from_user.id)
                if deposit < 100:
                    bot.send_message(message.chat.id,
                                     f"{username}, минимальный вклад 100 лисокойнов. Попробуйте снова или завершите операцию.",
                                     reply_markup=deposit_inline_buttons)
                elif int(deposit * 0.8) + last_deposit > 5000:
                    bot.send_message(message.chat.id,
                                     f"{username}, недостаточно места в банке, вы можете положить еще {int((5000 - last_deposit) / 0.8)}",
                                     reply_markup=deposit_inline_buttons)
                else:
                    if isWithdraw != 1:
                        if deposit <= balance:
                            in_trade_set_deposit(message.from_user.id, int(last_deposit + deposit - deposit * 0.2))
                            in_trade_set_deposit(-1, in_trade_get_deposit(-1) + (deposit * 0.2))
                            in_trade_set_coefficient(message.from_user.id, coefficient)
                            in_user_set_isDeposit(message.from_user.id, 0)
                            in_user_set_balance(message.from_user.id, balance - deposit)
                            name_coin = get_name_coin(int(deposit / coefficient))
                            bot.reply_to(message,
                                         f"Успех! Лисокойны вложены в банк под {coefficient}%. Сейчас ваш банк составляет {int(last_deposit + deposit - deposit * 0.2)} {name_coin}.")
                        else:
                            bot.send_message(message.chat.id,
                                             f"{username}, недостаточно лисокойнов, введите другое количество.",
                                             reply_markup=deposit_inline_buttons)
                    else:
                        bot.send_message(message.chat.id, f"@{username}, сначала завершите снятие.",
                                         reply_markup=withdraw_inline_buttons)
        except:
            bot.send_message(message.chat.id,
                             f"{username}, вклад должен быть числом. Попробуйте снова или завершите операцию.",
                             reply_markup=deposit_inline_buttons)
    except:
        pass


async def withdrawing(message, withdraw):
    try:
        deposit_inline_buttons = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton("Отменить вклад", callback_data="cancer_deposit"))
        withdraw_inline_buttons = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton("Отменить снятие", callback_data="cancer_withdraw"))
        isWithdraw = in_user_get_isWithdraw(message.from_user.id)
        username = in_user_get_username(message.from_user.id)
        try:
            if isWithdraw == 1:
                balance = in_user_get_balance(message.from_user.id)
                last_deposit = in_trade_get_deposit(message.from_user.id)
                isDeposit = in_user_get_isDeposit(message.from_user.id)
                coefficient = in_trade_get_coefficient(message.from_user.id)
                if isDeposit != 1:
                    if withdraw <= last_deposit:
                        in_trade_set_deposit(message.from_user.id, int(last_deposit - withdraw))
                        in_trade_set_coefficient(message.from_user.id, int(coefficient * 100) / 100)
                        in_user_set_isWithdraw(message.from_user.id, 0)
                        in_user_set_balance(message.from_user.id, int(balance + withdraw))
                        name_coin = get_name_coin(int(withdraw))
                        bot.reply_to(message, f"Успех! Вы забрали {int(withdraw)} {name_coin}.")
                    else:
                        bot.send_message(message.chat.id,
                                         f"{username}, в банке недостаточно лисокойнов, введите другое количество.",
                                         reply_markup=withdraw_inline_buttons)
                else:
                    bot.send_message(message.chat.id, f"{username}, сначала завершите вложение.",
                                     reply_markup=deposit_inline_buttons)
        except:
            bot.send_message(message.chat.id,
                             f"{username}, снятие должно быть числом. Попробуйте снова или завершите операцию.",
                             reply_markup=withdraw_inline_buttons)
    except:
        pass


async def cancer_deposit(message):
    try:
        username = in_user_get_username(message.from_user.id)
        in_user_set_isDeposit(message.from_user.id, 0)
        bot.send_message(message.from_user.id, f"{username}, вложение отменёно!")
    except:
        pass


async def cancer_withdraw(message):
    try:
        username = in_user_get_username(message.from_user.id)
        in_user_set_isWithdraw(message.from_user.id, 0)
        bot.send_message(message.from_user.id, f"{username}, снятие отменено!")
    except:
        pass


async def bank(message):
    try:
        bank = in_trade_get_deposit(message.from_user.id)
        name_coin = get_name_coin(bank)
        coefficient = int(in_trade_get_coefficient(message.from_user.id) * 100) / 100
        if bank != 0:
            bot.reply_to(message, f"В вашем банке {bank} {name_coin} под {coefficient}% в день.")
        else:
            bot.reply_to(message, f"В вашем банке {bank} {name_coin}.")
    except:
        pass


async def farm(user_id):
    try:
        if datetime.toordinal(datetime.now()) > get_farm_time(user_id):
            deposit = in_trade_get_deposit(user_id)
            coefficient = int(in_trade_get_coefficient(user_id) * 100) / 100
            if int(deposit * coefficient / 100 + deposit) <= 6000:
                in_trade_set_deposit(user_id, int(deposit * coefficient / 100 + deposit))
            else:
                in_trade_set_deposit(-1, in_trade_get_deposit(-1) + (int(deposit * coefficient / 100 + deposit) - 6000))
                in_trade_set_deposit(user_id, 6000)
            coefficient = in_trade_get_coefficient(-1)
            if coefficient < 0:
                coefficient = 0
            in_trade_set_coefficient(user_id, int(coefficient * 100) / 100)
            set_farm_time(user_id, datetime.toordinal(datetime.now()))
    except:
        pass

async def coef(chat_id):
    try:
        coefficient = in_trade_get_coefficient(-1)
        bot.send_message(chat_id, f"Текущий процент в банке {coefficient}%")
    except:
        pass
