from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot_token import token

bot = TeleBot(token)  # token = "token from botFather"


async def info(message, start):
    user_id = message.from_user.id
    inline_buttons = InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("Информация",
                             url='https://telegra.ph/Your-foxibot-Informaciya-09-30')).add(
        InlineKeyboardButton("Поддержать бота",
                             url='https://www.donationalerts.com/r/gert1m'))
    if not start:  # проверка, что команда вызвана не через старт
        if user_id != message.chat.id:  # проверка, что пользователь пишет не в лс бота
            bot.reply_to(message,
                         text="Информация отправлена в [ЛС бота](https://t.me/Your_foxibot)",
                         parse_mode='markdown')
            bot.send_message(user_id,
                             text="Информацию по использованию лсчк бота",
                             reply_markup=inline_buttons)
        bot.reply_to(message,
                     text="Информацию по использованию лсчк бота",
                     reply_markup=inline_buttons)
    else:
        bot.send_message(user_id,
                     text="Информацию по использованию лсчк бота",
                     reply_markup=inline_buttons)
