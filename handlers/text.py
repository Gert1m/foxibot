import asyncio
from event.attack import attack
from top.upgrade import upgrade_top
from trade.bank import bank, update_coefficient, coefficient
from trade.deposit import deposit
from trade.farm import farm
from trade.withdraw import withdraw
from upgrade.crit import crit
from upgrade.damage import damage
from upgrade.upgrade import upgrade
from upgrade.defence import defence
from user.admin_panel import admin_panel
from user.balance import balance
from user.info import info
from user.start import start
from user.vip import vip


async def any_text(message):
    text = message.text.lower().replace("@your_foxibot", "")  # наш текст
    await asyncio.gather(farm(message), update_coefficient())

    if len(text.split()) != 1 or len(text) > 10:  # не обрабатывать сообщения больше чем из 1 слова
        pass
    # user методы
    elif text.count("бал") + text.count("bal") != 0:
        await balance(message)  # баланс
    elif text.count("старт") + text.count("start") != 0:
        await start(message)  # старт
    elif text.count("инф") + text.count("info") != 0:
        await info(message, False)  # информация
    elif text.count("вип") + text.count("vip") != 0:
        await vip(message)  # вип

    # trade методы
    elif text.count("банк") + text.count("bank") != 0:
        await bank(message)  # банк
    elif text.count("коэф") + text.count("coef") != 0:
        await coefficient(message)  # коэффициент
    elif text.count("деп") + text.count("лож") + text.count("dep") != 0:
        await deposit(message)  # положить в банк
    elif text.count("виз") + text.count("снят") + text.count("withdraw") != 0:
        await withdraw(message)  # снять с банка

    # event методы
    elif text.count("атак") + text.count("рейд") + text.count("attack") != 0:
        await attack(message)  # рейд босса

    # top методы
    elif text.count("топ") + text.count("лидер") + text.count("top") != 0:
        await upgrade_top(message)

    # upgrade методы
    elif text.count("кач") + text.count("улучш") + text.count("upgrade") != 0:
        await upgrade(message)  # интерфейс улучшений
    elif text.count("урон") + text.count("атк") + text.count("атака") + text.count("atk") != 0:
        if text.count("++") != 0:
            await damage(message, f"+")  # улучшений урона пока не кончатся деньги
        elif text.count("+") != 0 and text.split("+")[-1].isdigit():  # проверка, что текст после '+' является числом
            await damage(message, int(text.split("+")[-1]))  # несколько улучшений урона
        else:
            await damage(message)  # информация про улучшение урона
    elif text.count("дэф") + text.count("щит") + text.count("def") != 0:
        if text.count("++") != 0:
            await defence(message, f"+")  # улучшений защиты пока не кончатся деньги
        elif text.count("+") != 0 and text.split("+")[-1].isdigit():  # проверка, что текст после '+' является числом
            await defence(message, int(text.split("+")[-1]))  # несколько улучшений защиты
        else:
            await defence(message)  # информация про улучшение защиты
    elif text.count("крит") + text.count("точн") + text.count("crit") != 0:
        if text.count("++") != 0:
            await crit(message, f"+")  # улучшений точности пока не кончатся деньги
        elif text.count("+") != 0 and text.split("+")[-1].isdigit():  # проверка, что текст после '+' является числом
            await crit(message, int(text.split("+")[-1]))  # несколько улучшений точности
        else:
            await crit(message)  # информация про улучшение точности

    if len(text.split()) != 2 or len(text) > 15:  # не обрабатывать сообщения состоящие не из 2 слова
        pass
    # моментальные trade методы
    elif text.count("деп") + text.count("лож") + text.count("dep") != 0 and text.split()[-1].isdigit:
        await deposit(message, text.split()[-1])  # положить в банк
    elif text.count("виз") + text.count("снят") + text.count("withdraw") != 0 and text.split()[-1].isdigit:
        await withdraw(message, text.split()[-1])  # снять с банка

    # admin_panel
    if text.split()[0] in ['set', 'get', 'say']:
        await admin_panel(message)
