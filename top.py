from telebot import types

from db import *
from bot_token import token

bot = token


def myFunc(value):
    return int(value[0])


async def top(message):
    keyboard = types.InlineKeyboardMarkup()
    kb1 = types.InlineKeyboardButton(text=" ", callback_data=" ")
    kb2 = types.InlineKeyboardButton(text="ребитх", callback_data="rebith_top")
    kb3 = types.InlineKeyboardButton(text=">>>", callback_data="balance_top")
    keyboard.row(kb1, kb2, kb3)
    top_rebith = list()
    text_with_top = "Топ пользователей по ребитхам:\n"
    top = get_all_from_db("user", "", "*")
    for row in top:
        row = str(row[-1]) + " " + str(row[0])
        top_rebith.append(str(row))

    top_rebith.sort()
    for i in range(10):
        username = get_from_db("user", "username", int(top_rebith[-i - 1].split()[-1]))
        text_with_top = text_with_top + f"[{username}](https://t.me/{username})" + " - " + top_rebith[-i - 1].split()[
            -2] + f" ребитх{get_name_coin(int(top_rebith[-i - 1].split()[-2]))}\n"

    bot.reply_to(message, text=text_with_top, reply_markup=keyboard, parse_mode='markdown')


async def rebith_top(message):
    keyboard = types.InlineKeyboardMarkup()
    kb1 = types.InlineKeyboardButton(text=" ", callback_data=" ")
    kb2 = types.InlineKeyboardButton(text="ребитх", callback_data="rebith_top")
    kb3 = types.InlineKeyboardButton(text=">>>", callback_data="balance_top")
    keyboard.add(kb1, kb2, kb3)
    top_rebith = list()
    text_with_top = "Топ пользователей по ребитхам:\n"
    top = get_all_from_db("user", "", "*")
    for row in top:
        row = (str(row[-1]) + " " + str(row[0])).split()
        top_rebith.append(row)

    top_rebith.sort(key=myFunc)
    for i in range(10):
        username = get_from_db("user", "username", int(top_rebith[-i - 1][-1]))
        text_with_top = text_with_top + f"[{username}](https://t.me/{username})" + " - " + top_rebith[-i - 1][
            -2] + f" ребитх{get_name_coin(int(top_rebith[-i - 1][-2]))}\n"

    bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text=text_with_top,
                          reply_markup=keyboard, parse_mode='markdown')


def balance_top(message):
    keyboard = types.InlineKeyboardMarkup()
    kb1 = types.InlineKeyboardButton(text="<<<", callback_data="rebith_top")
    kb2 = types.InlineKeyboardButton(text="баланс", callback_data="balance_top")
    kb3 = types.InlineKeyboardButton(text=">>>", callback_data="deposit_top")
    keyboard.add(kb1, kb2, kb3)
    top_balance = list()
    text_with_top = "Топ пользователей по балансу:\n"
    top = get_all_from_db("user", "", "*")
    for row in top:
        row = (str(row[-3]) + " " + str(row[0])).split()

        top_balance.append(row)

    top_balance.sort(key=myFunc)
    for i in range(10):
        username = get_from_db("user", "username", int(top_balance[-i - 1][-1]))
        text_with_top = text_with_top + f"[{username}](https://t.me/{username})" + " - " + top_balance[-i - 1][
            -2] + f" лисокойн{get_name_coin(int(top_balance[-i - 1][-2]))}\n"

    bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text=text_with_top,
                          reply_markup=keyboard, parse_mode='markdown')


def deposit_top(message):
    keyboard = types.InlineKeyboardMarkup()
    kb1 = types.InlineKeyboardButton(text="<<<", callback_data="balance_top")
    kb2 = types.InlineKeyboardButton(text="банк", callback_data="deposit_top")
    kb3 = types.InlineKeyboardButton(text=" ", callback_data=" ")
    keyboard.add(kb1, kb2, kb3)
    top_deposit = list()
    text_with_top = "Топ пользователей по банку:\n"
    top = get_all_from_db("trade", "", "*")
    for row in top:
        row = (str(row[2]) + " " + str(row[0])).split()

        top_deposit.append(row)

    top_deposit.sort(key=myFunc)
    for i in range(10):
        username = get_from_db("trade", "username", int(top_deposit[-i - 2][-1]))
        text_with_top = text_with_top + f"[{username}](https://t.me/{username})" + " - " + top_deposit[-i - 2][
            0] + f" лисокойн{get_name_coin(int(top_deposit[-i - 2][0]))}\n"

    bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text=text_with_top,
                          reply_markup=keyboard, parse_mode='markdown')