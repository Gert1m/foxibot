from telebot import TeleBot
from db import *
from bot_token import token

bot = TeleBot(token)  # token = "token from botFather"


async def balance(message):
    user_id = message.from_user.id
    my_balance = int(get_from_db("user", "balance", user_id))

    bot.reply_to(message, f"Ваш баланс составляет {my_balance} {"лисокойн" + get_name_coin(my_balance)}")
