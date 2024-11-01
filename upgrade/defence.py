from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from db import *
from bot_token import token

bot = TeleBot(token)  # token = "token from botFather"


async def defence(message, n=None):
    user_id = message.from_user.id
    lvlDef = int(get_from_db("upgrade", "lvlDef", user_id))
    balance = int(get_from_db("user", "balance", user_id))
    x = (2 * 1 + (218 / 249) * (lvlDef - 1)) / 2  # x = 1->110 при 250
    costDef = int(240 * (1.65 ** x))

    if n is None:  # вывод справки
        await defence_info(message, lvlDef, costDef, balance)
    elif n == "+":  # бесконечное улучшение
        total_upgrade = 0
        total_cost = costDef
        while balance >= total_cost:
            total_upgrade += 1

            x = (2 * 1 + (218 / 249) * (lvlDef + total_upgrade - 1)) / 2  # x = 1->110 при 250
            costDef = int(240 * (1.65 ** x))
            total_cost += costDef
        total_cost -= costDef

        set_in_db("user", "balance", f"{balance - total_cost}", user_id)
        set_in_db("upgrade", "lvlDef", f"{lvlDef + total_upgrade}", user_id)
        bot.reply_to(message,
                     f"Успешно произведено {total_upgrade} улучшений защиты\n"
                     f"Потрачено {total_cost} лисокойн{get_name_coin(total_cost)}")
        total_spent = int(get_from_db("upgrade", "total_spent", user_id))
        set_in_db("upgrade", "total_spent", f"{total_spent + total_cost}", user_id)
    elif n > 0:  # n количество улучшений
        total_cost = costDef
        for i in range(1, n + 1):
            x = (2 * 1 + (218 / 249) * (lvlDef + n - 1)) / 2  # x = 1->110 при 250
            costDef = int(240 * (1.65 ** x))
            total_cost += costDef
        total_cost -= costDef

        if balance < total_cost:
            bot.reply_to(message,
                         f"Вам не хватает лисокойнов на такое количество улучшений защиты")
        else:
            set_in_db("user", "balance", f"{balance - total_cost}", user_id)
            set_in_db("upgrade", "lvlDef", f"{lvlDef + n}", user_id)
            bot.reply_to(message,
                         f"Успешно произведено {n} улучшений защиты\n"
                         f"Потрачено {total_cost} лисокойн{get_name_coin(total_cost)}")
            total_spent = int(get_from_db("upgrade", "total_spent", user_id))
            set_in_db("upgrade", "total_spent", f"{total_spent + total_cost}", user_id)
    else:
        bot.reply_to(message,
                     f"Количество улучшений должно быть больше 0")


async def defence_info(message, lvlDef, costDef, balance):
    multi = (5 + lvlDef)
    change = 100 - int(1 / (lvlDef // 5 + 2) * 10000) / 100

    costDef = f"Цена улучшения: {costDef} лисокойн{get_name_coin(costDef)}"

    info_text = (f"Улучшение защиты увеличивает вашу скрытность о босса и максимальную серию ударов\n"
                 f"Текущая максимальная серия ударов = {multi}\n"
                 f"Шанс уклонится: {change}%\n\n"
                 f"Чтобы улучшить защиты напишите:\n"
                 "`защита+`{число} или \n"
                 "`защита++` (улучшение пока не кончится баланс)\n"
                 f"{costDef}\n"
                 f"Ваш баланс: {balance} лисокойн{get_name_coin(balance)}")

    try:
        bot.reply_to(message, text=info_text, parse_mode='markdown')
    except AttributeError:
        call = message
        buttons = InlineKeyboardMarkup()
        inline_button = InlineKeyboardButton("↩️ назад к улучшениям", callback_data=f"upgrade_{call.from_user.id}")
        buttons.row(inline_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"{info_text}", parse_mode='markdown', reply_markup=buttons)
