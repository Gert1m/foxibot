from db import *
from bot_token import token

bot = token


async def top(message):
    top_rebith = list()
    text_with_top = "Топ пользователей по ребитхам:\n"
    top = get_all_from_db("user", "", "*")
    for row in top:
        row = str(row[-1]) + " " + str(row[0])
        top_rebith.append(str(row))

    top_rebith.sort()
    for i in range(5):
        username = get_from_db("user", "username", f"{int(top_rebith[-i - 1].split()[-1])}")
        text_with_top = text_with_top + "@" + username + " - " + top_rebith[-i - 1].split()[
            -2] + f" ребитх{get_name_coin(int(top_rebith[-i - 1].split()[-2]))}\n"

    bot.send_message(message.chat.id, text=text_with_top)
