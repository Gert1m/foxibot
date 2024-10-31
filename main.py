import asyncio

from telebot import TeleBot
from bot_token import token
from handlers.callback import any_callback
from handlers.text import any_text

bot = TeleBot(token)  # token = "token from botFather"


@bot.message_handler(content_types=['text'])
def any_text_handler(message):
    try:
        asyncio.run(any_text(message))  # обработка всего текста
    except Exception as text_error:
        print(f"text_error: {text_error}")  # вывод ошибки в консоль в случае сбоя


@bot.callback_query_handler(func=lambda call: True)
def any_callback_handler(call):
    try:
        if call.from_user.id == call.message.reply_to_message.from_user.id:  # проверка, что инлайн кнопку нажал не сторонний человек
            asyncio.run(any_callback(call))  # обработка всех инлайн кнопок
    except Exception as callback_error:
        print(f"callback_error: {callback_error}")  # вывод ошибки в консоль в случае сбоя


if __name__ == "__main__":
    bot.polling(interval=1)
