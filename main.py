import asyncio

from invistition import *
from user import *

bot = token


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        user_id = call.from_user.id
        if int(get_from_db("user", "isVip", user_id)) == -1:
            bot.send_message(user_id, "Пользователь заблокирован!")
            set_in_db("user", "isVip", f"{-2}", user_id)
        elif int(get_from_db("user", "isVip", user_id)) in range(0, 3):
            if call.message:
                if call.data == "cancer_deposit" and int(get_from_db("user", "isDeposit", user_id)) != 0:
                    asyncio.run(cancer_deposit(call))
                if call.data == "cancer_withdraw" and int(get_from_db("user", "isWithdraw", user_id)) != 0:
                    asyncio.run(cancer_withdraw(call))
    except:
        pass


@bot.message_handler(content_types='text')
def any_text(message):
    try:
        user_id = message.from_user.id
        text = message.text.lower().replace("ё", 'е').split("@")[0]
        isVip = int(get_from_db("user", "isVip", user_id))

        if text == "/start":
            try:
                if float(get_from_db("user", "version", message.from_user.id)) == 1.1:
                    bot.reply_to(message, "У вас установлена последняя версия.")

                else:
                    asyncio.run(add_user(message))
            except:
                asyncio.run(add_user(message))

        if isVip == -1:
            bot.send_message(message.from_user.id, "Пользователь заблокирован!")
            set_in_db("user", "isVip", f"{-2}", user_id)

        elif isVip in range(0, 3):
            asyncio.run(farm(user_id))

            if text.isdigit():
                asyncio.run(depositing(message, int(message.text)))
                asyncio.run(withdrawing(message, int(message.text)))

            elif int(get_from_db("user", "isDeposit", user_id)) == 1:
                set_in_db("user", "isDeposit", f"{0}", user_id)

            elif int(get_from_db("user", "isWithdraw", user_id)) == 1:
                set_in_db("user", "isWithdraw", f"{0}", user_id)

            if text in ['кошель', 'баланс', 'кошелек', '/wallet']:
                asyncio.run(balance(message))

            if len(text.split()) == 2:
                if text.split()[0] in ['положить', 'внести', '/deposit'] and \
                        text.split()[1].isdigit():
                    set_in_db("user", "isDeposit", f"{1}", user_id)
                    asyncio.run(depositing(message, int(text.split()[1])))
                    set_in_db("user", "isDeposit", f"{0}", user_id)

                elif message.text.lower().split()[0] in ['/withdraw', 'снять', 'забрать'] and \
                        message.text.split()[1].isdigit():
                    set_in_db("user", "isWithdraw", f"{1}", user_id)
                    asyncio.run(withdrawing(message, int(message.text.split()[1])))
                    set_in_db("user", "isWithdraw", f"{0}", user_id)

            if text in ['положить', 'внести', '/deposit']:
                asyncio.run(trading())
                asyncio.run(deposit(message))

            if text in ['снять', 'забрать', '/withdraw']:
                asyncio.run(withdraw(message))

            if text in ['счет', 'банк', 'вклад', '/bank']:
                asyncio.run(bank(message))

            if text in ['коэфф', 'коэффициент', '/coef']:
                asyncio.run(trading())
                asyncio.run(coef(message))

            if text in ['/info', 'инфо', 'информация']:
                asyncio.run(information(message))

            if int(get_from_db("user", "isVip", user_id)) == 2:
                try:
                    if text.split()[0] == "/set":
                        set_in_db(f"{text.split()[1]}", f"{text.split()[2]}", f"{text.split()[3]}",
                                  message.reply_to_message.from_user.id if message.reply_to_message else int(
                                      text.split()[4]))
                        bot.reply_to(message, "Пользователь обновлён.")
                    if text.split()[0] == "/get":
                        bot.reply_to(message, get_from_db(f"{text.split()[1]}", f"{text.split()[2]}",
                                                          message.reply_to_message.from_user.id if message.reply_to_message else int(
                                                              text.split()[3])))
                except:
                    bot.reply_to(message, "Пользователя нет в базе данных.")

    except:
        pass


bot.polling()
