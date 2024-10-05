from asyncio import sleep

from bot_token import token
from db import *
from time import time
from random import randint

bot = token


async def wait(message):
    user_id = message.from_user.id
    if ((int(get_from_db("boss", "attack_time", user_id)) - int(time())) // 60) % 1 == 1:
        name_time = "минуту"

    elif ((int(get_from_db("boss", "attack_time", user_id)) - int(time())) // 60) % 1 in range(2, 5):
        name_time = "минуты"

    else:
        name_time = "минут"

    if ((int(get_from_db("boss", "attack_time", user_id)) - int(time())) % 60) % 1 == 1:
        seconds = "секунду"

    elif ((int(get_from_db("boss", "attack_time", user_id)) - int(time())) % 60) % 1 in range(2, 5):
        seconds = "секунды"

    else:
        seconds = "секунд"

    bot.reply_to(message,
                 f"Подождите еще {(int(get_from_db("boss", "attack_time", user_id)) - int(time())) // 60} {name_time} {(int(get_from_db("boss", "attack_time", user_id)) - int(time())) % 60} {seconds}")


async def attack(message):
    user_id = message.from_user.id
    isVip = int(get_from_db("user", "isVip", user_id))
    isPlaying = randint(1, 10 + 5 * isVip)
    combo = int(get_from_db("boss", "combo", user_id))
    combo_mp = int(combo / 3) if combo >= 3 else 1
    if int(get_from_db("boss", "damage", -1)) <= 0:
        await boss_reward()

    elif isPlaying != 1:
        crit_hit = randint(1, 10)
        set_in_db("boss", "combo", f"{combo + 1}", user_id)
        set_in_db("boss", "damage",
                  f"{(1 * combo_mp if crit_hit != 1 else 2 * combo_mp) + int(get_from_db("boss", "damage", user_id))}",
                  user_id)
        set_in_db("boss", "damage",
                  f"{int(get_from_db("boss", "damage", -1)) - (1 * combo_mp if crit_hit != 1 else 2 * combo_mp)}",
                  -1)
        await sleep(0.1)
        await attack(message)

    else:
        username = get_from_db("user", "username", user_id)
        damage = int(get_from_db("boss", "damage", user_id))
        bot.send_message(message.chat.id,
                         f"{username}, вы боролись изо всех сил, но сегодня зло победило добро. Подождите немного времени и возьмите реванш у босса!\n\nНанесённый урон: {damage}\nКоличество успешных атак: {combo}")
        set_in_db("boss",
                  "reward",
                  f"{int(get_from_db("boss", "damage", user_id)) + int(get_from_db("boss", "reward", user_id))}",
                  user_id)
        set_in_db("boss", "combo", f"{0}", user_id)
        set_in_db("boss", "damage", f"{0}", user_id)


async def boss_reward():
    player_list = get_all_from_db("boss", "", "id")
    for i in range(len(player_list)):
        if int(str(player_list[i])[1:-2])>0 and int(get_from_db("boss", "reward", int(str(player_list[i])[1:-2])))>0:
            user_id = int(str(player_list[i])[1:-2])
            bot.send_message(user_id, "Босс повержен! Все пользователи получили награду.")
            set_in_db("user", "balance",
                      f"{int(get_from_db("user", "balance", user_id)) + int(get_from_db("boss", "reward", user_id))}",
                      user_id)
            set_in_db("boss", "reward", f"{0}", user_id)
            set_in_db("boss", "attack_time", f"{0}", user_id)
            set_in_db("boss", "combo", f"{0}", user_id)
            set_in_db("boss", "damage", f"{0}", user_id)
    set_in_db("boss", "damage", f"{1000}", -1)

async def boss(message):
    boss_hp = int(get_from_db("boss", "damage", -1))
    bot.reply_to(message, f"Текущее хп босса: {boss_hp}")

async def reward(message):
    reward = int(get_from_db("boss", "reward", message.from_user.id))
    name_coin = get_name_coin(reward)
    bot.reply_to(message, f"После победы над боссом вы получите {reward} {name_coin}")
