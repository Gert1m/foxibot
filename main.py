import asyncio

from invistition import *
from bot_token import token

bot = token


async def add_user(message):
    try:
        add_in_db("user", "id", f"{message.from_user.id}")
        if message.from_user.username is None:
            set_in_db("user", "username", f"{message.from_user.first_name}", message.from_user.id)
        else:
            set_in_db("user", "username", f"{message.from_user.username}", message.from_user.id)

        add_in_db("trade", "id", f"{message.from_user.id}")
        if message.from_user.username is None:
            set_in_db("trade", "username", f"{message.from_user.first_name}", message.from_user.id)
        else:
            set_in_db("trade", "username", f"{message.from_user.username}", message.from_user.id)
        set_in_db("user", "version", f"{1.1}", message.from_user.id)
        bot.send_message(message.chat.id, "Обновление установлено!")
        await information(message)
    except:
        pass


async def balance(message):
    try:
        user_id = message.from_user.id
        balance = int(get_from_db("user", "balance", user_id))
        name_coin = get_name_coin(balance)
        bot.reply_to(message, f"Ваш баланс составляет {balance} {name_coin}")
    except:
        bot.reply_to(message, "Упс.. что-то пошло не так. Попробуйте позже.")


async def information(message):
    try:
        version = float(get_from_db("user", "version", message.from_user.id))
        if version != 1.1:
            text = "Вы используете старую версию бота, некоторые функции могут быть недоступны.\n\nЧтобы обновится до последней версии напишите /start"
        else:
            text = "У вас последняя версия бота."
        inline_buttons = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton("Информация",
                                       url='https://telegra.ph/Your-foxibot-Informaciya-09-30')).add(
            types.InlineKeyboardButton("Поддержать бота",
                                       url='https://www.donationalerts.com/r/gert1m'))
        bot.send_message(message.chat.id, f"Информация по использованию лсчк бота.\n{text}",
                         reply_markup=inline_buttons)
    except:
        pass


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        user_id = call.from_user.id
        user_chat = call.message.chat.id
        if int(get_from_db("user", "isVip", user_id)) == -1:
            bot.send_message(user_id, "Пользователь заблокирован!")
            set_in_db("user", "isVip", f"{-2}", user_id)
        elif int(get_from_db("user", "isVip", user_id)) in range(0, 2):
            if call.message:
                if call.data == "deposit" and int(get_from_db("user", "isWithdraw", user_id)) != 1:
                    asyncio.run(deposit(user_id, user_chat))
                if call.data == "withdraw" and int(get_from_db("user", "isDeposit", user_id)) != 1:
                    asyncio.run(withdraw(call.from_user.id, user_chat))
                if call.data == "cancer_deposit" and int(get_from_db("user", "isDeposit", user_id)) != 0:
                    asyncio.run(cancer_deposit(call))
                if call.data == "cancer_withdraw" and int(get_from_db("user", "isWithdraw", user_id)) != 0:
                    asyncio.run(cancer_withdraw(call))
    except:
        pass


@bot.message_handler(commands=['start'])
def start_command(message):
    try:
        if float(get_from_db("user", "version", message.from_user.id)) == 1.1:
            bot.reply_to(message, "У вас установлена последняя версия.")
        else:
            asyncio.run(add_user(message))
    except:
        asyncio.run(add_user(message))


@bot.message_handler(content_types='text')
def any_text(message):
    try:
        user_id = message.from_user.id
        text = message.text.lower().replace("ё", 'е').split("@")[0]

        if int(get_from_db("user", "isVip", user_id)) == -1:
            bot.send_message(message.from_user.id, "Пользователь заблокирован!")
            set_in_db("user", "isVip", f"{-2}", user_id)
        elif int(get_from_db("user", "isVip", user_id)) in range(0, 2):

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
                try:
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
                except:
                    pass

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

    except:
        pass


bot.polling()
