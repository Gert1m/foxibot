from bot_token import token
from db import *
from telebot import types

bot = token


async def add_user(message):
    add_in_db("user", "id", f"{message.from_user.id}")
    if message.from_user.username is None:
        set_in_db("user", "username", f"{message.from_user.first_name}", message.from_user.id)

    else:
        set_in_db("user", "username", f"{message.from_user.username}", message.from_user.id)

    add_in_db("trade", "id", f"{message.from_user.id}")
    if message.from_user.username is None:
        set_in_db("trade", "username", f"{message.from_user.first_name}", message.from_user.id)

    else:
        set_in_db("trade", "username", f"{message.from_user.username}", message.from_user.id)

    add_in_db("boss", "id", f"{message.from_user.id}")
    if message.from_user.username is None:
        set_in_db("boss", "username", f"{message.from_user.first_name}", message.from_user.id)

    else:
        set_in_db("boss", "username", f"{message.from_user.username}", message.from_user.id)

    set_in_db("user", "version", f"{1.2}", message.from_user.id)
    bot.send_message(message.chat.id, "Обновление установлено!")
    await information(message)


async def balance(message):
    user_id = message.from_user.id
    balance = int(get_from_db("user", "balance", user_id))
    name_coin = get_name_coin(balance)
    bot.reply_to(message, f"Ваш баланс составляет {balance} {name_coin}")


async def information(message):
    version = float(get_from_db("user", "version", message.from_user.id))
    if version != 1.1:
        text = "Вы используете старую версию бота, некоторые функции могут быть недоступны.\n\nЧтобы обновится до последней версии напишите /start"
    else:
        text = "У вас последняя версия бота."
    inline_buttons = types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton("Информация",
                                   url='https://telegra.ph/Your-foxibot-Informaciya-09-30')).add(
        types.InlineKeyboardButton("Поддержать бота",
                                   url='https://www.donationalerts.com/r/gert1m'))
    bot.send_message(message.chat.id, f"Информация по использованию лсчк бота.\n{text}",
                     reply_markup=inline_buttons)
