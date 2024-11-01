from time import time
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot_token import token
from db import *
from random import randint

bot = TeleBot(token)  # token = "token from botFather"


async def attack(message):
    user_id = message.from_user.id
    lvlDmg = int(get_from_db("upgrade", "lvlDmg", user_id))
    lvlDef = int(get_from_db("upgrade", "lvlDef", user_id))
    lvlCrit = int(get_from_db("upgrade", "lvlCrit", user_id))
    isVip = int(get_from_db("user", "isVip", user_id))
    next_attack = int(get_from_db("boss", "attack_time", user_id))

    vip_save = 1 if isVip != 0 else 0

    n = 2 + lvlDef // 5  # удар с шансом 50% +~6.25% за каждые 5 уровней защиты
    if time() >= next_attack:
        next_attack = int(time()) + (2700 if isVip != 0 else 3600)
        set_in_db("boss", "attack_time", f"{next_attack}", user_id)
        isPlaying = randint(1, int(n))

        combo = 0
        total_damage = 0
        my_logs = "Информация по рейду:\n"

        while (isPlaying != 1 or vip_save > 0) and combo < 5 + lvlDef:
            crit_hit = randint(0, 100) if lvlCrit != 0 else 0  # если уровень шанса крита 0, то и шанс 0%
            value = randint(1, 50)

            last_hit = int(value * (1 + lvlDmg / 10))  # +10% c каждого уровня прокачки урона
            if crit_hit in range(1, int(((2 * 5 + (190 / 29) * (lvlCrit - 1)) / 2))):
                isCrit = True
                last_hit = int((value * (1 + lvlDmg / 10)) * 1.5)  # и +50% за крит удар
            else:
                isCrit = False

            total_damage += last_hit
            combo += 1
            if isPlaying == 1 and vip_save != 0:
                vip_save = 0
                my_logs += "вип спасение...\n"
            my_logs += f"{combo}: {"критический удар на" if isCrit else "обычный удар на"} {last_hit}\n"
            isPlaying = randint(1, int(n))

        my_logs += f"Суммарный урон {total_damage}"
        if isVip != 0:
            set_in_db("boss", "logs", f"{my_logs}", user_id)
        else:
            set_in_db("boss", "logs", f"{None}", user_id)

        balance = int(get_from_db("user", "balance", user_id))
        combo = f"Серия из {combo} удар{get_name_coin(combo) if combo % 10 != 1 else "а"}" if combo < lvlDef + 5 else "Максимальная серия ударов"

        buttons = InlineKeyboardMarkup()
        inline_button = InlineKeyboardButton("Как все прошло?", callback_data=f"logs_{user_id}")
        buttons.row(inline_button)

        bot.reply_to(message,
                     f"{combo}\n"
                     f"Урон: {total_damage}",
                     reply_markup=buttons)

        set_in_db("user", "balance", f"{balance + total_damage}", user_id)
    else:
        await wait(message, next_attack)


async def wait(message, next_attack):
    if (next_attack - int(time()) // 60) % 1 == 1:
        name_time = "минуту"

    elif (next_attack - int(time()) // 60) % 1 in range(2, 5):
        name_time = "минуты"

    else:
        name_time = "минут"

    if (next_attack - int(time()) % 60) % 1 == 1:
        seconds = "секунду"

    elif (next_attack - int(time()) % 60) % 1 in range(2, 5):
        seconds = "секунды"

    else:
        seconds = "секунд"

    bot.reply_to(message,
                 f"Недавно вы уже совершали нападение подождите еще {(next_attack - int(time())) // 60} {name_time} {(next_attack - int(time())) % 60} {seconds}")


async def logs(call):
    user_id = call.from_user.id
    my_logs = get_from_db("boss", "logs", user_id)
    if my_logs == "None":
        my_logs = "Информация по рейду доступна только вип пользователям"
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=my_logs)
    elif str(my_logs).split()[-1] == str(call.message.text).split()[-1]:
        bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=my_logs)
    else:
        my_logs = "Информация недоступна"
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=my_logs)
