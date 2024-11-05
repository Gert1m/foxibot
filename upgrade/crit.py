from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from db import *
from bot_token import token

bot = TeleBot(token)  # token = "token from botFather"


async def crit(message, n=None):
    def get_cost(lvl_upgrade):
        value = (3 - (21 / 1450) * (lvl_upgrade - 1)) / 2  # x = 1.5->1.29
        return int(120 * (value ** lvl_upgrade))

    user_id = message.from_user.id
    lvlCrit = int(get_from_db("upgrade", "lvlCrit", user_id))
    balance = int(get_from_db("user", "balance", user_id))
    costCrit = get_cost(lvlCrit)

    if n is None:  # вывод справки
        await crit_info(message, lvlCrit, costCrit, balance)
    elif lvlCrit >= 30:  # проверка на ур точности
        bot.reply_to(message,
                     f"Точность улучшена на максимум, теперь вы можете бить даже с закрытыми глазами...")
    elif n == "+":  # бесконечное улучшение
        total_upgrade = 0
        total_cost = costCrit
        while balance >= total_cost:
            total_upgrade += 1

            if lvlCrit + total_upgrade >= 30:  # проверка на ур точности
                bot.reply_to(message,
                             f"Точность будет улучшена на максимум, теперь вы можете бить даже с закрытыми глазами...")
                break
            costCrit = get_cost(lvlCrit + total_upgrade)
            total_cost += costCrit
        total_cost -= costCrit

        set_in_db("user", "balance", f"{balance - total_cost}", user_id)
        set_in_db("upgrade", "lvlCrit", f"{lvlCrit + total_upgrade}", user_id)
        bot.reply_to(message,
                     f"Успешно произведено {total_upgrade} улучшений точности\n"
                     f"Потрачено {total_cost} лисокойн{get_name_coin(total_cost)}")
        total_spent = int(get_from_db("upgrade", "total_spent", user_id))
        set_in_db("upgrade", "total_spent", f"{total_spent + total_cost}", user_id)
    elif n > 0:  # n количество улучшений
        total_cost = costCrit
        if lvlCrit + n >= 30:
            n = 30 - lvlCrit
            bot.reply_to(message,
                         f"Точность будет улучшена на максимум, теперь вы сможете бить даже с закрытыми глазами...")
        for i in range(1, n + 1):
            costCrit = get_cost(lvlCrit + i)
            total_cost += costCrit
        total_cost -= costCrit

        if balance < total_cost:
            bot.reply_to(message,
                         f"Вам не хватает лисокойнов на такое количество улучшений точности")
        else:
            set_in_db("upgrade", "lvlCrit", f"{lvlCrit + n}", user_id)
            set_in_db("user", "balance", f"{balance - total_cost}", user_id)
            bot.reply_to(message,
                         f"Успешно произведено {n} улучшений точности\n"
                         f"Потрачено {total_cost} лисокойн{get_name_coin(total_cost)}")
            total_spent = int(get_from_db("upgrade", "total_spent", user_id))
            set_in_db("upgrade", "total_spent", f"{total_spent + total_cost}", user_id)
    else:
        bot.reply_to(message,
                     f"Количество улучшений должно быть больше 0")


async def crit_info(message, lvlCrit, costCrit, balance):
    change = int(((2 * 5 + (190 / 29) * (lvlCrit - 1)) / 2)) if lvlCrit > 0 else 0

    if lvlCrit >= 30:  # проверка на ур точности
        costCrit = f"Цена улучшения: макс. ур"
    else:
        costCrit = f"Цена улучшения: {costCrit} лисокойн{get_name_coin(costCrit)}"

    info_text = (f"Улучшение точности увеличивает ваш шанс нанести критический удар по боссу\n"
                 f"Текущий шанс крит. удара = {change}%\n\n"
                 f"Чтобы улучшить точность напишите:\n"
                 "`точность+`{число} или \n"
                 "`точность++` (улучшение пока не кончится баланс)\n"
                 f"{costCrit}\n"
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
