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
    bot.reply_to(message, "Бот обновлён, информация по использованию отправлена в лс бота.", parse_mode='html')
    await information(message)


async def balance(message):
    user_id = message.from_user.id
    balance = int(get_from_db("user", "balance", user_id))
    bot.reply_to(message, f"Ваш баланс составляет {balance} {"лисокойн" + get_name_coin(balance)}")


async def information(message):
    inline_buttons = types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton("Информация",
                                   url='https://telegra.ph/Your-foxibot-Informaciya-09-30')).add(
        types.InlineKeyboardButton("Поддержать бота",
                                   url='https://www.donationalerts.com/r/gert1m'))
    bot.reply_to(message, "Информация отправлена в [лс](https://t.me/Your_foxibot) бота", parse_mode='markdown')
    bot.send_message(message.from_user.id, f"Информация по использованию лсчк бота.",
                     reply_markup=inline_buttons)


async def vip(message):
    user_id = message.from_user.id
    bot.reply_to(message, "Информация отправлена в [лс](https://t.me/Your_foxibot) бота", parse_mode='markdown')
    inline_buttons = types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton("Привилегии вип пользователя",
                                   url='https://telegra.ph/Your-foxibot-vip-info-10-05'))
    if int(get_from_db("user", "isVip", user_id)) < 1:
        inline_buttons = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton("Привилегии вип пользователя",
                                       url='https://telegra.ph/Your-foxibot-vip-info-10-05')).add(
            types.InlineKeyboardButton("Купить вип",
                                       url='https://www.donationalerts.com/r/gert1m'))
    bot.send_message(user_id,
                     f"Информация про вип статус. {"\nВы вип пользователь!" if int(get_from_db("user", "isVip", user_id)) > 0 else ""}",
                     reply_markup=inline_buttons)
