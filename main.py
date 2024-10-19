import asyncio

from invistition import *
from user import *
from boss import *
from top import *

bot = token


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        user_id = call.from_user.id
        if int(get_from_db("user", "isVip", user_id)) == -1:
            bot.send_message(user_id, "Пользователь заблокирован!")
            set_in_db("user", "isVip", f"{-2}", user_id)

        elif int(get_from_db("user", "isVip", user_id)) in range(0, 3):
            if call.from_user.id == call.message.reply_to_message.from_user.id:
                if call.message:
                    if call.data == "upgrade":
                        asyncio.run(upgrade(call.message.reply_to_message))
                        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

                    elif call.data == "crit_up":
                        asyncio.run(crit_up(call))

                    elif call.data == "damage_up":
                        asyncio.run(damage_up(call))

                    elif call.data == "vision_up":
                        asyncio.run(vision_up(call))

                    elif call.data == "crit":
                        buttons = types.InlineKeyboardMarkup(row_width=1).add(
                            types.InlineKeyboardButton("Подтвердить", callback_data="crit_up")).add(
                            types.InlineKeyboardButton("Отмена", callback_data="upgrade"))
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text="Вы точно хотите увеличить крит. шанс?", reply_markup=buttons)

                    elif call.data == "damage":
                        buttons = types.InlineKeyboardMarkup(row_width=1).add(
                            types.InlineKeyboardButton("Подтвердить", callback_data="damage_up")).add(
                            types.InlineKeyboardButton("Отмена", callback_data="upgrade"))
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text="Вы точно хотите увеличить урон?", reply_markup=buttons)

                    elif call.data == "vision":
                        buttons = types.InlineKeyboardMarkup(row_width=1).add(
                            types.InlineKeyboardButton("Подтвердить", callback_data="vision_up")).add(
                            types.InlineKeyboardButton("Отмена", callback_data="upgrade"))
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text="Вы точно хотите увеличить скрытность?", reply_markup=buttons)

                    elif call.data == "cancer_deposit" and int(get_from_db("trade", "isDeposit", user_id)) != 0:
                        asyncio.run(cancer_deposit(call))

                    elif call.data == "cancer_withdraw" and int(get_from_db("trade", "isWithdraw", user_id)) != 0:
                        asyncio.run(cancer_withdraw(call))

                    elif call.data == "rebith":
                        asyncio.run(do_rebith(call))

                    elif call.data == "claim_reward" and int(get_from_db("boss", "reward", user_id)) > 0:
                        user_id = call.from_user.id
                        set_in_db("user", "balance",
                                  f"{int(get_from_db("user", "balance", user_id)) + int(get_from_db("boss", "reward", user_id))//3}",
                                  user_id)
                        set_in_db("boss", "reward", f"{0}", user_id)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text=f"{get_from_db("user", "username", user_id)}, награда собрана!")

                    elif call.data == "rebith_top":
                        asyncio.run(rebith_top(call))
                    elif call.data == "balance_top":
                        asyncio.run(balance_top(call))
                    elif call.data == "deposit_top":
                        asyncio.run(deposit_top(call))

    except:
        pass


@bot.message_handler(content_types='text')
def any_text(message):
    try:
        user_id = message.from_user.id
        text = message.text.lower().replace("ё", 'е').replace("@your_foxibot", "")

        if text == "/start":
            asyncio.run(add_user(message))

        elif text == "/vip":
            asyncio.run(vip(message))

        elif text == "/top":
            asyncio.run(top(message))

        isVip = int(get_from_db("user", "isVip", user_id))
        if isVip == -1:
            bot.send_message(message.from_user.id, "Пользователь заблокирован!")
            set_in_db("user", "isVip", f"{-2}", user_id)

        elif isVip in range(0, 3):
            asyncio.run(farm(user_id))

            if text.isdigit():
                asyncio.run(depositing(message, int(message.text)))
                asyncio.run(withdrawing(message, int(message.text)))

            elif int(get_from_db("trade", "isDeposit", user_id)) == 1:
                set_in_db("trade", "isDeposit", f"{0}", user_id)

            elif int(get_from_db("trade", "isWithdraw", user_id)) == 1:
                set_in_db("trade", "isWithdraw", f"{0}", user_id)

            if text in ['кошель', 'баланс', 'кошелек', '/wallet']:
                asyncio.run(balance(message))

            elif len(text.split()) == 2:
                if text.split()[0] in ['положить', 'внести', '/deposit'] and \
                        text.split()[1].isdigit():
                    set_in_db("trade", "isDeposit", f"{1}", user_id)
                    asyncio.run(depositing(message, int(text.split()[1])))
                    set_in_db("trade", "isDeposit", f"{0}", user_id)

                elif message.text.lower().split()[0] in ['/withdraw', 'снять', 'забрать'] and \
                        message.text.split()[1].isdigit():
                    set_in_db("trade", "isWithdraw", f"{1}", user_id)
                    asyncio.run(withdrawing(message, int(message.text.split()[1])))
                    set_in_db("trade", "isWithdraw", f"{0}", user_id)

            elif text in ['урон+']:
                asyncio.run(damage_up(message))

            elif text in ['точность+']:
                asyncio.run(crit_up(message))

            elif text in ['скрытность+']:
                asyncio.run(vision_up(message))

            elif text in ['ребитх', '/rebirth']:
                asyncio.run(rebith(message))

            elif text in ['ребитх+']:
                asyncio.run(do_rebith(message))

            elif text in ['положить', 'внести', '/deposit']:
                asyncio.run(trading())
                asyncio.run(deposit(message))

            elif text in ['снять', 'забрать', '/withdraw']:
                asyncio.run(withdraw(message))

            elif text in ['счет', 'банк', 'вклад', '/bank']:
                asyncio.run(bank(message))

            elif text in ['коэфф', 'коэффициент', '/coef']:
                asyncio.run(trading())
                asyncio.run(coef(message))

            elif text in ['/info', 'инфо', 'информация']:
                asyncio.run(information(message))

            elif text in ['/boss', 'босс']:
                asyncio.run(boss(message))

            elif text in ['/attack', 'бить', 'рейд', 'атака']:
                lvlVision = int(get_from_db("boss", "lvlVision", user_id))
                lvlDamage = int(get_from_db("boss", "lvlDamage", user_id))
                lvlCrit = int(get_from_db("boss", "lvlCrit", user_id))
                balance_ = int(get_from_db("user", "balance", user_id))
                rebith_ = int(get_from_db("user", "rebith", user_id))
                if int(time()) > int(get_from_db("boss", "attack_time", user_id)):
                    if lvlVision == 5 and lvlCrit == 10 and lvlDamage == 10 and balance_ > (
                            450 + 450 * (1 + rebith_ / 10 * 3)):
                        bot.reply_to(message,
                                     f"В целях баланса системы вы не можете бить босса если вам хватает на ребитх, пожалуйста сделайте ребитх.")
                    else:
                        set_in_db("boss", "attack_time",
                                  f"{int(time()) + (3600 - 900 * isVip)}", user_id)
                        asyncio.run(attack(message))
                else:
                    asyncio.run(wait(message))

            elif text in ['/reward', 'награда']:
                asyncio.run(reward(message))

            elif text in ['/upgrade', 'улучшить']:
                asyncio.run(upgrade(message))

            if int(get_from_db("user", "isVip", user_id)) == 2:
                try:
                    if text.split()[0] == "/set":
                        set_in_db(f"{text.split()[1]}", f"{text.split()[2]}", f"{text.split()[3]}",
                                  message.reply_to_message.from_user.id if message.reply_to_message else int(
                                      text.split()[4]))
                        bot.reply_to(message, "Пользователь обновлён.")
                    elif text.split()[0] == "/get":
                        bot.reply_to(message, get_from_db(f"{text.split()[1]}", f"{text.split()[2]}",
                                                          message.reply_to_message.from_user.id if message.reply_to_message else int(
                                                              text.split()[3])))
                    elif text.split()[0] == "/say":
                        bot.send_message(text.split()[1], f"{text.split(" ", maxsplit=2)[2]}")
                except:
                    bot.reply_to(message, "Пользователя нет в базе данных.")

    except:
        pass


bot.polling()
