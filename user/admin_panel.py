from telebot import TeleBot
from telebot.apihelper import ApiTelegramException

from db import *
from bot_token import token
from sqlite3 import OperationalError

bot = TeleBot(token)  # token = "token from botFather"


async def admin_panel(message):
    user_id = message.from_user.id
    text = message.text.lower().split()  # наш текст
    if text[1] not in ['boss', 'trade', 'upgrade', 'user'] and text[0] in ['get', 'set']:
        bot.reply_to(message, f"Нет такого файла {text[1]}")
    elif int(get_from_db("user", "isVip", user_id)) > 1:
        try:
            if text[0] == "set":
                if str(text[3]).count("+") != 0:
                    value = int(get_from_db(f"{text[1]}", f"{text[2]}",
                                            message.reply_to_message.from_user.id if message.reply_to_message else int(
                                                text[4])))
                    value2 = int(str(text[3]).split("+")[-1])
                    set_in_db(f"{text[1]}", f"{text[2]}", f"{value + value2}",
                              message.reply_to_message.from_user.id if message.reply_to_message else int(
                                  text[4]))
                else:
                    set_in_db(f"{text[1]}", f"{text[2]}", f"{text[3]}",
                              message.reply_to_message.from_user.id if message.reply_to_message else int(
                                  text[4]))
                bot.reply_to(message, "Пользователь обновлён.")
            elif text[0] == "get":
                value = get_from_db(f"{text[1]}", f"{text[2]}",
                                    message.reply_to_message.from_user.id if message.reply_to_message else int(
                                        text[3]))
                bot.reply_to(message, text=value)
            elif text[0] == "say":
                text = message.text.lower()
                bot.send_message(text.split()[1], f"{text.split(" ", maxsplit=2)[2]}")
                bot.reply_to(message, "Сообщение отправлено")
        except OperationalError:
            bot.reply_to(message, f"Нет такой таблицы {text[2]}")
        except TypeError:
            bot.reply_to(message, "Пользователя нет в базе данных")
        except ValueError:
            bot.reply_to(message, "Неверный ввод литерала")
        except ApiTelegramException:
            bot.reply_to(message, "Пользователя не зарегистрирован в боте")
