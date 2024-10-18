from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

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
    rebith = int(get_from_db("user", "rebith", user_id))
    lvlDamage = int(get_from_db("boss", "lvlDamage", user_id))
    lvlVision = int(get_from_db("boss", "lvlVision", user_id))
    lvlCrit = int(get_from_db("boss", "lvlCrit", user_id))
    isVip = int(get_from_db("user", "isVip", user_id))
    isPlaying = randint(1, int(10 + 2 * lvlVision) if isVip <= 0 else int((10 + 2 * lvlVision) * 1.5))
    combo = int(get_from_db("boss", "combo", user_id))
    combo_mp = int(combo / 3) if combo >= 3 else 1
    if int(get_from_db("boss", "damage", -1)) <= 0:
        username = get_from_db("user", "username", user_id)
        damage = int(get_from_db("boss", "damage", user_id))
        bot.reply_to(message,
                     f"{username}, вы убили босса!\nНанесённый урон: {damage}\nКоличество успешных атак: {combo}")
        set_in_db("boss",
                  "reward",
                  f"{int((int(get_from_db("boss", "damage", user_id)) + int(get_from_db("boss", "reward", user_id))) * (1 + rebith / 10))}",
                  user_id)
        await boss_reward()

    elif isPlaying != 1:
        crit_hit = randint(1, 11 - lvlCrit)
        set_in_db("boss", "combo", f"{combo + 1}", user_id)
        set_in_db("boss", "damage",
                  f"{((1 + lvlDamage) * combo_mp if crit_hit != 1 else (2 + lvlDamage) * combo_mp) + int(get_from_db("boss", "damage", user_id))}",
                  user_id)
        set_in_db("boss", "damage",
                  f"{int(get_from_db("boss", "damage", -1)) - ((1 + lvlDamage) * combo_mp if crit_hit != 1 else (2 + lvlDamage) * combo_mp)}",
                  -1)
        await attack(message)

    else:
        username = get_from_db("user", "username", user_id)
        damage = int(get_from_db("boss", "damage", user_id))
        bot.reply_to(message,
                     f"{username}, вы боролись изо всех сил, но сегодня зло победило добро. Подождите немного времени и возьмите реванш у босса!\n\nНанесённый урон: {damage}\nКоличество успешных атак: {combo}")
        set_in_db("boss",
                  "reward",
                  f"{int((int(get_from_db("boss", "damage", user_id)) + int(get_from_db("boss", "reward", user_id))) * (1 + rebith / 10))}",
                  user_id)
        set_in_db("boss", "combo", f"{0}", user_id)
        set_in_db("boss", "damage", f"{0}", user_id)


async def boss_reward():
    player_list = get_all_from_db("boss", "", "id")
    for i in range(len(player_list)):
        if int(str(player_list[i])[1:-2]) > 0 and int(
                get_from_db("boss", "reward", int(str(player_list[i])[1:-2]))) > 0:
            user_id = int(str(player_list[i])[1:-2])
            try:
                bot.send_message(user_id, "Босс повержен! Все пользователи получили награду.")
            except:
                pass
            set_in_db("user", "balance",
                      f"{int(get_from_db("user", "balance", user_id)) + int(get_from_db("boss", "reward", user_id)) // 10}",
                      user_id)
            set_in_db("boss", "reward", f"{0}", user_id)
            set_in_db("boss", "combo", f"{0}", user_id)
            set_in_db("boss", "damage", f"{0}", user_id)
    count = int(str(get_all_from_db("boss", "COUNT", "(id)")[0])[1:-2])
    set_in_db("boss", "damage", f"{randint(4, 10) * 100 * count}", -1)


async def upgrade(message):
    user_id = message.from_user.id
    rebith = int(get_from_db("user", "rebith", user_id))

    lvlDamage = int(get_from_db("boss", "lvlDamage", user_id))
    lvlVision = int(get_from_db("boss", "lvlVision", user_id))
    lvlCrit = int(get_from_db("boss", "lvlCrit", user_id))

    set_in_db("boss", "costCrit", f"{int(120 * (1.5 ** lvlCrit)) * (1 + rebith / 4)}", user_id)
    set_in_db("boss", "costVision", f"{int(240 * (1.5 **    lvlVision)) * (1 + rebith / 4)}", user_id)
    set_in_db("boss", "costDamage", f"{int(90 * (1.5 ** lvlDamage)) * (1 + rebith / 4)}", user_id)

    costDamage = int(get_from_db("boss", "costDamage", user_id))
    costVision = int(get_from_db("boss", "costVision", user_id))
    costCrit = int(get_from_db("boss", "costCrit", user_id))

    buttons = InlineKeyboardMarkup()

    damage_button = InlineKeyboardButton("🔪" if lvlDamage < 10 else "✅",
                                         callback_data=("damage" if lvlDamage < 10 else " "))
    vision_button = InlineKeyboardButton("🛡️" if lvlVision < 5 else "✅",
                                         callback_data=("vision" if lvlVision < 5 else " "))
    crit_button = InlineKeyboardButton("🎯" if lvlCrit < 10 else "✅",
                                       callback_data=("crit" if lvlCrit < 10 else " "))

    buttons.row(damage_button, vision_button, crit_button)
    text = (
               f"Урон {lvlDamage}/10 ") + (
               f"цена: {costDamage} {"лисокойн" + get_name_coin(costDamage)}." if lvlDamage < 10 else "Максимальное улучшение.") + (
               f"\nСкрытность {lvlVision}/5 ") + (
               f"цена: {costVision} {"лисокойн" + get_name_coin(costVision)}" if lvlVision < 5 else "Максимальное улучшение.") + (
               f"\nТочность {lvlCrit}/10 ") + (
               f"цена: {costCrit} {"лисокойн" + get_name_coin(costCrit)}." if lvlCrit < 10 else "Максимальное улучшение."
           )
    bot.reply_to(message, text=text, reply_markup=buttons)


async def crit_up(message):
    user_id = message.from_user.id
    rebith = int(get_from_db("user", "rebith", user_id))
    lvlCrit = int(get_from_db("boss", "lvlCrit", user_id))
    costCrit = int(get_from_db("boss", "costCrit", user_id))
    balance = int(get_from_db("user", "balance", user_id))
    buttons = InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("Другие улучшения", callback_data="upgrade"))

    if balance > costCrit:
        set_in_db("user", "balance", f"{balance - int(120 * (1.5 ** (lvlCrit + 1))) * (1 + rebith / 4)}", user_id)
        set_in_db("boss", "costCrit", f"{int(120 * (1.5 ** (lvlCrit + 1))) * (1 + rebith / 4)}", user_id)
        set_in_db("boss", "lvlCrit", f"{lvlCrit + 1}", user_id)
        try:
            bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text="Успех!",
                                  reply_markup=buttons)
        except:
            bot.reply_to(message, "Успех!", reply_markup=buttons)
    else:
        try:
            bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                  text="Недостаточно лисокойнов.", reply_markup=buttons)
        except:
            bot.reply_to(message, "Недостаточно лисокойнов.", reply_markup=buttons)


async def vision_up(message):
    user_id = message.from_user.id
    rebith = int(get_from_db("user", "rebith", user_id))
    lvlVision = int(get_from_db("boss", "lvlVision", user_id))
    costVision = int(get_from_db("boss", "costVision", user_id))
    balance = int(get_from_db("user", "balance", user_id))
    buttons = InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("Другие улучшения", callback_data="upgrade"))

    if balance > costVision:
        set_in_db("user", "balance", f"{balance - int(240 * (1.5 ** (lvlVision + 1))) * (1 + rebith / 4)}", user_id)
        set_in_db("boss", "costVision", f"{int(240 * (1.5 ** (lvlVision + 1))) * (1 + rebith / 4)}", user_id)
        set_in_db("boss", "lvlVision", f"{lvlVision + 1}", user_id)
        try:
            bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text="Успех!",
                                  reply_markup=buttons)
        except:
            bot.reply_to(message, "Успех!", reply_markup=buttons)
    else:
        try:
            bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                  text="Недостаточно лисокойнов.", reply_markup=buttons)
        except:
            bot.reply_to(message, "Недостаточно лисокойнов.", reply_markup=buttons)


async def damage_up(message):
    user_id = message.from_user.id
    rebith = int(get_from_db("user", "rebith", user_id))
    balance = int(get_from_db("user", "balance", user_id))
    lvlDamage = int(get_from_db("boss", "lvlDamage", user_id))
    costDamage = int(get_from_db("boss", "costDamage", user_id))
    buttons = InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("Другие улучшения", callback_data="upgrade"))

    if balance > costDamage:
        set_in_db("user", "balance", f"{balance - int(90 * (1.5 ** (lvlDamage + 1))) * (1 + rebith / 4)}", user_id)
        set_in_db("boss", "costDamage", f"{int(90 * (1.5 ** (lvlDamage + 1))) * (1 + rebith / 4)}", user_id)
        set_in_db("boss", "lvlDamage", f"{lvlDamage + 1}", user_id)
        try:
            bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text="Успех!",
                                  reply_markup=buttons)
        except:
            bot.reply_to(message, "Успех!", reply_markup=buttons)
    else:
        try:
            bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                  text="Недостаточно лисокойнов.", reply_markup=buttons)
        except:
            bot.reply_to(message, "Недостаточно лисокойнов.", reply_markup=buttons)


async def rebith(message):
    buttons = InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("Подтвердить", callback_data="rebith"))
    user_id = message.from_user.id
    lvlVision = int(get_from_db("boss", "lvlVision", user_id))
    lvlDamage = int(get_from_db("boss", "lvlDamage", user_id))
    lvlCrit = int(get_from_db("boss", "lvlCrit", user_id))
    rebith = int(get_from_db("user", "rebith", user_id))

    bot.reply_to(message, f"Вы сделали {rebith} ребитх{get_name_coin(rebith)}")

    if lvlVision == 5 and lvlCrit == 10 and lvlDamage == 10:
        bot.reply_to(message,
                     f"Вы хотите сделать ребитх? Это сбросит весь ваш текущий прогресс но даст небольшой бонус в дальнейшем.\nЦена ребитха {450 + 450 * (1 + rebith / 10 * 3)}.",
                     reply_markap=buttons)
    else:
        bot.reply_to(message, f"Чтобы сделать ребитх надо сначала улучшить все атрибуты в /upgrade до максимума.")


async def do_rebith(message):
    user_id = message.from_user.id
    balance = int(get_from_db("user", "balance", user_id))
    rebith = int(get_from_db("user", "rebith", user_id))
    lvlVision = int(get_from_db("boss", "lvlVision", user_id))
    lvlDamage = int(get_from_db("boss", "lvlDamage", user_id))
    lvlCrit = int(get_from_db("boss", "lvlCrit", user_id))

    if lvlVision == 5 and lvlCrit == 10 and lvlDamage == 10:
        if balance >= (450 + 450 * (1 + rebith / 10 * 3)):
            set_in_db("user", "balance", f"{balance - (450 + 450 * (1 + rebith / 10 * 3))}", user_id)
            set_in_db("user", "rebith", f"{rebith + 1}", user_id)
            set_in_db("boss", "attack_time", f"{0}", user_id)
            set_in_db("boss", "lvlVision", f"{0}", user_id)
            set_in_db("boss", "lvlDamage", f"{0}", user_id)
            set_in_db("boss", "lvlCrit", f"{0}", user_id)
            set_in_db("user", "balance", f"{0}", user_id)
            try:
                bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                      text="Успех!.")
            except:
                bot.reply_to(message, "Успех!")
        else:
            try:
                bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                      text="Недостаточно лисокойнов.")
            except:
                bot.reply_to(message, "Недостаточно лисокойнов.")
    else:
        bot.reply_to(message, f"Чтобы сделать ребитх надо сначала улучшить все атрибуты в /upgrade до максимума.")


async def boss(message):
    boss_hp = int(get_from_db("boss", "damage", -1))
    bot.reply_to(message, f"Текущее хп босса: {boss_hp}")


async def reward(message):
    buttons = InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("Забрать досрочно", callback_data="claim_reward"))
    user_id = message.from_user.id
    reward = int(get_from_db("boss", "reward", user_id))
    if reward > 0:
        bot.reply_to(message,
                     f"После победы над боссом вы получите {reward // 10} {"лисокойн" + get_name_coin(reward // 10)}",
                     reply_markup=buttons)
    else:
        bot.reply_to(message,
                     f"После победы над боссом вы получите {reward // 10} {"лисокойн" + get_name_coin(reward // 10)}", )
