from telebot import types, TeleBot
from db import *
from bot_token import token

bot = TeleBot(token)  # token = "token from botFather"


def myFunc(value):
    return int(value[0])


async def upgrade_top(message):
    my_top = list()
    db_top = get_all_from_db("upgrade", "", "*")
    for row in db_top:
        row = f"{row[-1]} {row[1]} {row[2]} {row[3]} {row[0]}".split()
        my_top.append(row)

    top_with_text = ("Топ пользователей по улучшениям\n"
                     "№. *Имя*: *урон* | *крит* | *защита*\n")

    my_top.sort(key=myFunc)
    for i in range(10):
        value = my_top[-i - 1]
        username = get_from_db("user", "username", int(value[-1]))
        vip_status = "💎" if int(get_from_db("user", "isVip", int(value[-1]))) != 0 else " "
        top_with_text += f"{i+1}. {vip_status} [{username}](https://t.me/{username}): {value[1]} | {value[2]} | {value[3]}\n"

    bot.reply_to(message, text=top_with_text, parse_mode='markdown', disable_web_page_preview=True)
