import asyncio

from invistition import *
from report import report_user

bot = token


async def main_def():
    async def add_user(message):
        try:
            add_id('user', message.from_user.id)
            if message.from_user.username is None:
                in_user_set_username(message.from_user.id, f"{message.from_user.first_name}")
            else:
                in_user_set_username(message.from_user.id, f"{message.from_user.username}")

            add_id('trade', message.from_user.id)
            if message.from_user.username is None:
                in_trade_set_username(message.from_user.id, f"{message.from_user.first_name}")
            else:
                in_trade_set_username(message.from_user.id, f"{message.from_user.username}")
            set_version(message.from_user.id, 1.1)
            bot.send_message(message.chat.id, "Обновление установлено!")
            await information(message)
        except:
            pass

    def balance(user_id, chat_id):
        try:
            balance = in_user_get_balance(user_id)
            name_coin = get_name_coin(balance)
            bot.send_message(chat_id, f"Ваш баланс составляет {balance} {name_coin}")
        except:
            bot.send_message(chat_id, "Упс.. что-то пошло не так. Попробуйте позже.")

    async def update_user_username(message):
        try:
            if in_user_get_username(message.from_user.id) == 'None':
                in_user_set_username(message.from_user.id, f"{message.from_user.first_name}")
                in_trade_set_username(message.from_user.id, f"{message.from_user.first_name}")
            elif in_user_get_username(message.from_user.id) != 'None':
                in_user_set_username(message.from_user.id, f"{message.from_user.username}")
                in_trade_set_username(message.from_user.id, f"{message.from_user.username}")
        except:
            pass

    async def information(message):
        try:
            version = get_version(message.from_user.id)
            if version != 1.1:
                text = "Вы используете старую версию бота, некоторые функции могут быть недоступны.\n\nЧтобы обновится до последней версии напишите /start"
            else:
                text = "У вас последняя версия бота."
            inline_buttons = types.InlineKeyboardMarkup(row_width=1).add(
                types.InlineKeyboardButton("Информация",
                                           url='https://telegra.ph/Your-foxibot-Informaciya-09-30')).add(
                types.InlineKeyboardButton("Поддержать бота",
                                           url='https://www.donationalerts.com/r/gert1m'))
            bot.send_message(message.chat.id, f"Информация по использованию лсчк бота.\n{text}", reply_markup=inline_buttons)
        except:
            pass

    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        try:
            if in_user_get_isVip(call.from_user.id) == -1:
                bot.send_message(call.from_user.id, "Пользователь заблокирован!")
                in_user_set_isVip(call.from_user.id, -2)
            elif in_user_get_isVip(call.from_user.id) in range(0, 2):
                if call.message:
                    if call.data == "deposit" and in_user_get_isDeposit(call.from_user.id) != 1:
                        asyncio.run(deposit(call.from_user.id, call.message.chat.id))
                    if call.data == "withdraw" and in_user_get_isWithdraw(call.from_user.id) != 1:
                        asyncio.run(withdraw(call.from_user.id, call.message.chat.id))
                    if call.data == "cancer_deposit" and in_user_get_isDeposit(call.from_user.id) != 0:
                        asyncio.run(cancer_deposit(call))
                    if call.data == "cancer_withdraw" and in_user_get_isWithdraw(call.from_user.id) != 0:
                        asyncio.run(cancer_withdraw(call))
        except:
            pass

    @bot.message_handler(commands=['start'])
    def start_command(message):
        try:
            if get_version(message.from_user.id) == 1.1:
                bot.reply_to(message, "У вас установлена последняя версия.")
            else:
                asyncio.run(add_user(message))
        except:
            asyncio.run(add_user(message))

    @bot.message_handler(content_types='text')
    def any_text(message):
        try:
            if in_user_get_isVip(message.from_user.id) == -1:
                bot.send_message(message.from_user.id, "Пользователь заблокирован!")
                in_user_set_isVip(message.from_user.id, -2)
            elif in_user_get_isVip(message.from_user.id) in range(0, 2):
                asyncio.run(farm(message.from_user.id))
                if message.text.isdigit():
                    asyncio.run(depositing(message, int(message.text)))
                    asyncio.run(withdrawing(message, int(message.text)))
                elif in_user_get_isDeposit(message.from_user.id) == 1:
                    in_user_set_isDeposit(message.from_user.id, 0)
                elif in_user_get_isWithdraw(message.from_user.id) == 1:
                    in_user_set_isWithdraw(message.from_user.id, 0)
                if message.text.lower().replace("ё", 'е').split("@")[0] in ['кошель', 'баланс', 'кошелек', '/wallet']:
                    balance(message.from_user.id, message.chat.id)
                if len(message.text.split()) == 2:
                    try:
                        if message.text.lower().split()[0] in ['положить', 'внести', '/deposit'] and \
                                message.text.split()[1].isdigit():
                            in_user_set_isDeposit(message.from_user.id, 1)
                            asyncio.run(depositing(message, int(message.text.split()[1])))
                            in_user_set_isDeposit(message.from_user.id, 0)
                        elif message.text.lower().split()[0] in ['/withdraw', 'снять', 'забрать'] and \
                                message.text.split()[1].isdigit():
                            in_user_set_isWithdraw(message.from_user.id, 1)
                            asyncio.run(withdrawing(message, int(message.text.split()[1])))
                            in_user_set_isWithdraw(message.from_user.id, 0)
                    except:
                        pass
                if message.text.lower().split("@")[0] in ['положить', 'внести', '/deposit']:
                    asyncio.run(trading())
                    asyncio.run(invistition(message))
                if message.text.lower().replace("ё", 'е').split("@")[0] in ['счет', 'банк', 'вклад', '/bank']:
                    asyncio.run(bank(message))
                if message.text.lower().split("@")[0] in ['коэфф', 'коэффициент', '/coef']:
                    asyncio.run(trading())
                    asyncio.run(coef(message.chat.id))
                if message.text.lower().split("@")[0] in ['/info', 'инфо', 'информация']:
                    asyncio.run(information(message))
                asyncio.run(update_user_username(message))
                if message.text.lower().split("@")[0] in ['/report', 'репорт']:
                    report_user(message)
        except:
            pass


asyncio.run(main_def())
bot.polling()
