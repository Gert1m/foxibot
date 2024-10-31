from telebot import TeleBot
from db import *
from user.info import info
from bot_token import token

bot = TeleBot(token)  # token = "token from botFather"


async def start(message):
    # добавляем пользователя во все базы данных
    add_in_db("user", "id", f"{message.from_user.id}")
    add_in_db("trade", "id", f"{message.from_user.id}")
    add_in_db("upgrade", "id", f"{message.from_user.id}")
    add_in_db("boss", "id", f"{message.from_user.id}")

    if message.from_user.username is None:  # проверка есть ли username у пользователя(нужно для топа)
        set_in_db("user", "username", f"{message.from_user.first_name}", message.from_user.id)
    else:
        set_in_db("user", "username", f"{message.from_user.username}", message.from_user.id)

    if message.from_user.id != message.chat.id:  # проверка, что пользователь пишет не в лс бота
        bot.reply_to(message,
                     text="Бот обновлён, информация по использованию отправлена в [ЛС бота](https://t.me/Your_foxibot).",
                     parse_mode='markdown')
    else:
        bot.reply_to(message,
                     text="Бот обновлён")

    await info(message, True)  # показываем документацию бота
