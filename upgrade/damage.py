from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from db import *
from bot_token import token

bot = TeleBot(token)  # token = "token from botFather"


async def damage(message, n=None):
    user_id = message.from_user.id
    lvlDmg = int(get_from_db("upgrade", "lvlDmg", user_id))
    balance = int(get_from_db("user", "balance", user_id))
    x = (2 * 1 + (148 / 499) * (lvlDmg - 1)) / 2  # x = 1->75 при 300
    costDmg = int(90 * (1.75 ** x))

    if n is None:  # вывод справки
        await damage_info(message, lvlDmg, costDmg, balance)
    elif n == "+":  # бесконечное улучшение
        total_upgrade = 0
        total_cost = costDmg
        while balance >= total_cost:
            total_upgrade += 1

            x = (2 * 1 + (148 / 499) * (lvlDmg + total_upgrade - 1)) / 2  # x = 1->75 при 300
            costDmg = int(90 * (1.75 ** x))
            total_cost += costDmg
        total_cost -= costDmg

        set_in_db("user", "balance", f"{balance - total_cost}", user_id)
        set_in_db("upgrade", "lvlDmg", f"{lvlDmg + total_upgrade}", user_id)
        bot.reply_to(message,
                     f"Успешно произведено {total_upgrade} улучшений урона\n"
                     f"Потрачено {total_cost} лисокойн{get_name_coin(total_cost)}")
        total_spent = int(get_from_db("upgrade", "total_spent", user_id))
        set_in_db("upgrade", "total_spent", f"{total_spent + total_cost}", user_id)
    elif n > 0:  # n количество улучшений
        total_cost = costDmg
        for i in range(1, n + 1):
            x = (2 * 1 + (148 / 499) * (lvlDmg + n - 1)) / 2  # x = 1->75 при 300
            costDmg = int(90 * (1.75 ** x))
            total_cost += costDmg
        total_cost -= costDmg

        if balance < total_cost:
            bot.reply_to(message,
                         f"Вам не хватает лисокойнов на такое количество улучшений урона")
        else:
            set_in_db("upgrade", "lvlDmg", f"{lvlDmg + n}", user_id)
            set_in_db("user", "balance", f"{balance - total_cost}", user_id)
            bot.reply_to(message,
                         f"Успешно произведено {n} улучшений урона\n"
                         f"Потрачено {total_cost} лисокойн{get_name_coin(total_cost)}")
            total_spent = int(get_from_db("upgrade", "total_spent", user_id))
            set_in_db("upgrade", "total_spent", f"{total_spent + total_cost}", user_id)
    else:
        bot.reply_to(message,
                     f"Количество улучшений должно быть больше 0")


async def damage_info(message, lvlDmg, costDmg, balance):
    multi = (1 + lvlDmg / 10)

    costDmg = f"Цена улучшения: {costDmg} лисокойн{get_name_coin(costDmg)}"

    info_text = (f"Улучшение урона увеличивает то с какой силой вы сможете ударить босса\n"
                 f"Текущий множитель удара удара = x{multi}\n\n"
                 f"Чтобы улучшить урон напишите:\n"
                 "`урон+`{число} или \n"
                 "`урон++` (улучшение пока не кончится баланс)\n"
                 f"{costDmg}\n"
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
