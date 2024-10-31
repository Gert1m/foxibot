from telebot import TeleBot
from db import *
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot_token import token

bot = TeleBot(token)  # token = "token from botFather"


async def vip(message):
    user_id = message.from_user.id

    if message.from_user.id != message.chat.id:  # проверка, что пользователь пишет не в лс бота
        bot.reply_to(message, "Информация отправлена в [ЛС бота](https://t.me/Your_foxibot)",
                     parse_mode='markdown')

    if int(get_from_db("user", "isVip", user_id)) < 1:  # проверка, что пользователь не vip
        vip_info_button = InlineKeyboardButton("Привилегии вип пользователя",
                                               url='https://telegra.ph/Your-foxibot-vip-info-10-05')
        vip_buy_button = InlineKeyboardButton("Купить вип",
                                              url='https://www.donationalerts.com/r/gert1m')
        inline_buttons = InlineKeyboardMarkup().row(vip_info_button, vip_buy_button)

    else:
        vip_info_button = InlineKeyboardButton("Привилегии вип пользователя",
                                               url='https://telegra.ph/Your-foxibot-vip-info-10-05')
        inline_buttons = InlineKeyboardMarkup().row(vip_info_button)

    bot.send_message(user_id,
                     f"Информация про вип статус. {"\nВы вип пользователь!" if int(get_from_db("user", "isVip", user_id)) > 0 else ""}",
                     reply_markup=inline_buttons)
