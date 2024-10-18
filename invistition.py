from datetime import datetime
from telebot import types
from db import *
from bot_token import token

bot = token


async def trading():
    value = int(str(get_all_from_db("trade", "SUM", "(deposit)")[0])[1:-2])
    count = int(str(get_all_from_db("trade", "COUNT", "(deposit)")[0])[1:-2])

    coefficient = (2000 - (int(value / (250 * count) * 100))) / 100

    if coefficient < 0:
        coefficient = 0
    set_in_db("trade", "coefficient", f"{coefficient}", -1)


async def deposit(message):
    user_id = message.from_user.id
    isVip = int(get_from_db("user", "isVip", user_id))
    deposit_inline_buttons = types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton("Отменить вклад", callback_data="cancer_deposit"))
    last_deposit = int(get_from_db("trade", "deposit", user_id))
    balance = int(get_from_db("user", "balance", user_id))

    if balance < 100:
        bot.reply_to(message, f"У вас недостаточно лисокойнов!")

    elif last_deposit >= 5000:
        bot.reply_to(message,
                     f"Недостаточно места в банке.")

    else:
        balance = int((5000 - last_deposit) / (0.8 if isVip <= 0 else 0.99))
        bot.reply_to(message, f"Введите сумму взноса до {balance} лисокойнов.",
                     reply_markup=deposit_inline_buttons)

        set_in_db("trade", "isDeposit", f"{1}", user_id)


async def withdraw(message):
    user_id = message.from_user.id
    withdraw_inline_buttons = types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton("Отменить снятие", callback_data="cancer_withdraw"))
    deposit = int(get_from_db("trade", "deposit", user_id))

    if deposit > 0:
        name_coin = get_name_coin(deposit)
        bot.reply_to(message,
                     f"Сколько лисокойнов хотите забрать из банка? На данный момент в банке хранится {deposit} {name_coin}.",
                     reply_markup=withdraw_inline_buttons)
        set_in_db("trade", "isWithdraw", f"{1}", user_id)

    else:
        bot.reply_to(message, f"В банке нет лисокойнов.")


async def depositing(message, deposit):
    user_id = message.from_user.id
    isVip = int(get_from_db("user", "isVip", user_id))
    deposit_inline_buttons = types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton("Отменить вклад", callback_data="cancer_deposit"))
    isDeposit = int(get_from_db("trade", "isDeposit", user_id))
    if isDeposit == 1:
        balance = int(get_from_db("user", "balance", user_id))
        last_deposit = int(get_from_db("trade", "deposit", user_id))
        coefficient = float(get_from_db("trade", "coefficient", -1))
        isWithdraw = int(get_from_db("trade", "isWithdraw", user_id))

        if deposit < 100:
            bot.reply_to(message,
                         f"Минимальный вклад 100 лисокойнов. Попробуйте снова или завершите операцию.",
                         reply_markup=deposit_inline_buttons)

        elif int(deposit * (0.8 if isVip <= 0 else 0.99)) + last_deposit > 5000:
            bot.reply_to(message,
                         f"Недостаточно места в банке, вы можете положить еще {int((5000 - last_deposit) / (0.8 if isVip <= 0 else 0.99)) if (int(deposit * (0.8 if isVip <= 0 else 0.99)) + last_deposit) <= 5000 else 0}",
                         reply_markup=deposit_inline_buttons)

        else:
            if isWithdraw != 1:
                if deposit <= balance:
                    set_in_db("trade", "deposit",
                              f"{int(last_deposit + deposit - deposit * (0.2 if isVip <= 0 else 0.01))}", user_id)
                    set_in_db("trade", "deposit",
                              f"{int(get_from_db("trade", "deposit", -1)) + int(deposit * (0.2 if isVip <= 0 else 0.01))}",
                              -1)
                    set_in_db("trade", "coefficient", f"{coefficient}", user_id)
                    set_in_db("trade", "isWithdraw", f"{0}", user_id)
                    set_in_db("user", "balance", f"{balance - deposit}", user_id)
                    name_coin = get_name_coin(int(deposit / coefficient))
                    bot.reply_to(message,
                                 f"Успех! Лисокойны вложены в банк под {coefficient}%. Сейчас ваш банк составляет {int(last_deposit + deposit - deposit * (0.2 if isVip <= 0 else 0.01))} {name_coin}.")

                else:
                    bot.reply_to(message,
                                 f"Недостаточно лисокойнов, введите другое количество.",
                                 reply_markup=deposit_inline_buttons)


async def withdrawing(message, withdraw):
    user_id = message.from_user.id
    withdraw_inline_buttons = types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton("Отменить снятие", callback_data="cancer_withdraw"))
    isWithdraw = int(get_from_db("trade", "isWithdraw", user_id))
    if isWithdraw == 1:
        balance = int(get_from_db("user", "balance", user_id))
        last_deposit = int(get_from_db("trade", "deposit", user_id))
        isDeposit = int(get_from_db("trade", "isDeposit", user_id))
        coefficient = float(get_from_db("trade", "coefficient", user_id))

        if isDeposit != 1:
            if withdraw <= last_deposit:
                set_in_db("trade", "deposit", f"{int(last_deposit - withdraw)}", user_id)
                set_in_db("trade", "coefficient", f"{int(coefficient * 100) / 100}", user_id)
                set_in_db("trade", "isWithdraw", f"{0}", user_id)
                set_in_db("user", "balance", f"{int(balance + withdraw)}", user_id)
                name_coin = get_name_coin(int(withdraw))
                bot.reply_to(message, f"Успех! Вы забрали {int(withdraw)} {name_coin}.")

            else:
                bot.reply_to(message,
                             f"В банке недостаточно лисокойнов, введите другое количество.",
                             reply_markup=withdraw_inline_buttons)


async def cancer_deposit(message):
    user_id = message.from_user.id
    username = get_from_db("user", "username", user_id)
    set_in_db("trade", "isDeposit", f"{0}", user_id)
    bot.send_message(message.message.chat.id, f"{username}, вложение отменёно!")


async def cancer_withdraw(message):
    user_id = message.from_user.id
    username = get_from_db("user", "username", user_id)
    set_in_db("trade", "isWithdraw", f"{0}", user_id)
    bot.send_message(message.message.chat.id, f"{username}, снятие отменено!")


async def bank(message):
    user_id = message.from_user.id
    bank = int(get_from_db("trade", "deposit", user_id))
    name_coin = get_name_coin(bank)
    coefficient = int(float(get_from_db("trade", "coefficient", user_id)) * 100) / 100
    if bank != 0:
        bot.reply_to(message, f"В вашем банке {bank} {name_coin} под {coefficient}% в день.")
    else:
        bot.reply_to(message, f"В вашем банке {bank} {name_coin}.")


async def farm(user_id):
    if datetime.toordinal(datetime.now()) > int(get_from_db("trade", "farm_time", user_id)):
        deposit = int(get_from_db("trade", "deposit", user_id))
        coefficient = int(float(get_from_db("trade", "coefficient", user_id)) * 100) / 100

        if int(deposit * coefficient / 100 + deposit) <= 6000:
            set_in_db("trade", "deposit", f"{int(deposit * coefficient / 100 + deposit)}", user_id)

        else:
            set_in_db("trade", "deposit",
                      f"{int(get_from_db("trade", "deposit", -1)) + int(deposit * coefficient / 100 + deposit) - 6000}",
                      -1)
            set_in_db("trade", "deposit", f"{6000}", user_id)

        coefficient = int(float(get_from_db("trade", "coefficient", -1)) * 100) / 100

        if coefficient < 0:
            coefficient = 0

        set_in_db("trade", "coefficient", f"{coefficient}", user_id)
        set_in_db("trade", "farm_time", f"{datetime.toordinal(datetime.now())}", user_id)


async def coef(message):
    coefficient = float(get_from_db("trade", "coefficient", -1))
    bot.reply_to(message, f"Текущий процент в банке {coefficient}%")
