from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from db import *
from bot_token import token

bot = TeleBot(token)  # token = "token from botFather"


async def upgrade(message):
    user_id = message.from_user.id
    lvlDamage = int(get_from_db("upgrade", "lvlDmg", user_id))
    lvlVision = int(get_from_db("upgrade", "lvlDef", user_id))
    lvlCrit = int(get_from_db("upgrade", "lvlCrit", user_id))

    buttons = InlineKeyboardMarkup()

    damage_button = InlineKeyboardButton("🔪", callback_data=f"damage_up_info_{user_id}")
    vision_button = InlineKeyboardButton("🛡️", callback_data=f"vision_up_info_{user_id}")
    crit_button = InlineKeyboardButton("🎯", callback_data=f"crit_uo_info_{user_id}")

    buttons.row(damage_button, vision_button, crit_button)
    upgrade_text = (
        f"Ваши характеристики:\n"
        f"🔪 Урон по боссу: {lvlDamage} ур\n"
        f"🛡️ Защита: {lvlVision} ур\n"
        f"🎯 Точность удара: {lvlCrit} ур\n"
        f"\nЧто делает каждая из характеристик можно узнать по кнопкам снизу")

    try:
        bot.reply_to(message, text=upgrade_text, reply_markup=buttons)
    except AttributeError:
        call = message
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=upgrade_text,
                          reply_markup=buttons)
