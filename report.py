from telebot import TeleBot

bot = TeleBot("7978670535:AAH8GcfngyqpSbPgE7W3Q_CkZ-EK09m7ORg")


def report_user(message):
    try:
        if message.from_user.username != message.reply_to_message.chat.username:
            report = str(
                "@" + message.from_user.username + " репортит @" + message.reply_to_message.from_user.username + "\nhttps://t.me/" + message.reply_to_message.chat.username + "/" + str(
                    message.reply_to_message.id))
        elif message.reply_to_message.chat.username is None:
            report = str(
                "@" + message.from_user.username + " репортит @" + message.reply_to_message.from_user.username + "\n" + message.reply_to_message.text)
        else:
            report = str("от @" + message.from_user.username + "\n\n" + message.reply_to_message.text)
        for i in [2121424181]:
            bot.send_message(i, report)
        bot.reply_to(message, "@" + message.from_user.username + " репорт отправлен!")
    except:
        pass
