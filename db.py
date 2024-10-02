import sqlite3


def get_name_coin(value: int):
    if value % 10 in [2, 3, 4]:
        name_coin = "лисокойна"
    elif value % 10 in [5, 6, 7, 8, 9, 0]:
        name_coin = "лисокойнов"
    else:
        name_coin = "лисокойн"
    return name_coin


def in_user_get_username(user_id: int):
    connect = sqlite3.connect("user.db")
    cursor = connect.cursor()
    cursor.execute(f"SELECT username FROM user WHERE id = {user_id}")
    username = str(cursor.fetchone())[1:-2]
    connect.close()
    return username[1:-1]


def in_user_get_balance(user_id: int):
    connect = sqlite3.connect("user.db")
    cursor = connect.cursor()
    cursor.execute(f"SELECT balance FROM user WHERE id = {user_id}")
    balance = int(str(cursor.fetchone())[1:-2])
    connect.close()
    return balance


def in_user_get_isVip(user_id: int):
    try:
        connect = sqlite3.connect("user.db")
        cursor = connect.cursor()
        cursor.execute(f"SELECT isVip FROM user WHERE id = {user_id}")
        isVip = int(str(cursor.fetchone())[1:-2])
        connect.close()
        return isVip
    except ValueError:
        return None


def in_user_get_isDeposit(user_id: int):
    connect = sqlite3.connect("user.db")
    cursor = connect.cursor()
    cursor.execute(f"SELECT isDeposit FROM user WHERE id = {user_id}")
    isDeposit = int(str(cursor.fetchone())[1:-2])
    connect.close()
    return isDeposit


def in_user_get_isWithdraw(user_id: int):
    connect = sqlite3.connect("user.db")
    cursor = connect.cursor()
    cursor.execute(f"SELECT isWithdraw FROM user WHERE id = {user_id}")
    isWithdraw = int(str(cursor.fetchone())[1:-2])
    connect.close()
    return isWithdraw


def in_user_set_username(user_id: int, username: str):
    connect = sqlite3.connect("user.db")
    cursor = connect.cursor()
    cursor.execute(f"UPDATE user SET username = '{username}' WHERE id = {user_id}")
    connect.commit()
    connect.close()


def in_user_set_isDeposit(user_id: int, isDeposit: int):
    connect = sqlite3.connect("user.db")
    cursor = connect.cursor()
    cursor.execute(f"UPDATE user SET isDeposit = {isDeposit} WHERE id = {user_id}")
    connect.commit()
    connect.close()


def in_user_set_isWithdraw(user_id: int, isWithdraw: int):
    connect = sqlite3.connect("user.db")
    cursor = connect.cursor()
    cursor.execute(f"UPDATE user SET isWithdraw = {isWithdraw} WHERE id = {user_id}")
    connect.commit()
    connect.close()


def in_user_set_isVip(user_id: int, isVip: int):
    connect = sqlite3.connect("user.db")
    cursor = connect.cursor()
    cursor.execute(f"UPDATE user SET isVip = {isVip} WHERE id = {user_id}")
    connect.commit()
    connect.close()


def in_user_set_balance(user_id: int, balance: int):
    connect = sqlite3.connect("user.db")
    cursor = connect.cursor()
    cursor.execute(f"UPDATE user SET balance = {balance} WHERE id = {user_id}")
    connect.commit()
    connect.close()


def add_id(table: str, user_id: int):
    try:
        connect = sqlite3.connect(f"{table}.db")
        cursor = connect.cursor()
        cursor.execute(f"INSERT INTO {table} (id) VALUES ({user_id})")
        connect.commit()
        connect.close()
    except:
        connect.close()


def in_trade_get_deposit(user_id: int):
    connect = sqlite3.connect("trade.db")
    cursor = connect.cursor()
    cursor.execute(f"SELECT deposit FROM trade WHERE id = {user_id}")
    deposit = int(str(cursor.fetchone())[1:-2])
    connect.close()
    return deposit


def in_trade_get_coefficient(user_id):
    connect = sqlite3.connect("trade.db")
    cursor = connect.cursor()
    cursor.execute(f"SELECT coefficient FROM trade WHERE id = {user_id}")
    coefficient = float(str(cursor.fetchone())[1:-2])
    connect.close()
    return coefficient


def in_trade_get_isTrading(user_id):
    connect = sqlite3.connect("trade.db")
    cursor = connect.cursor()
    cursor.execute(f"SELECT isTrading FROM trade WHERE id = {user_id}")
    isTrading = int(str(cursor.fetchone())[1:-2])
    connect.close()
    return isTrading


def get_farm_time(user_id: int):
    connect = sqlite3.connect("trade.db")
    cursor = connect.cursor()
    cursor.execute(f"SELECT farm_time FROM trade WHERE id = {user_id}")
    farm_time = int(str(cursor.fetchone())[1:-2])
    connect.close()
    return farm_time


def set_farm_time(user_id, farm_time: int):
    connect = sqlite3.connect("trade.db")
    cursor = connect.cursor()
    cursor.execute(f"UPDATE trade SET farm_time = {farm_time} WHERE id = {user_id}")
    connect.commit()
    connect.close()


def in_trade_set_coefficient(user_id: int, coefficient: float):
    connect = sqlite3.connect("trade.db")
    cursor = connect.cursor()
    cursor.execute(f"UPDATE trade SET coefficient = {coefficient} WHERE id = {user_id}")
    connect.commit()
    connect.close()


def in_trade_set_deposit(user_id: int, deposit: int):
    connect = sqlite3.connect("trade.db")
    cursor = connect.cursor()
    cursor.execute(f"UPDATE trade SET deposit = {deposit} WHERE id = {user_id}")
    connect.commit()
    connect.close()


def in_trade_set_isTrading(isTrading: int, user_id: int):
    connect = sqlite3.connect("trade.db")
    cursor = connect.cursor()
    cursor.execute(f"UPDATE trade SET isTrading = {isTrading} WHERE id = {user_id}")
    connect.commit()
    connect.close()


def in_trade_set_username(user_id: int, username: str):
    connect = sqlite3.connect("trade.db")
    cursor = connect.cursor()
    cursor.execute(f"UPDATE trade SET username = '{username}' WHERE id = {user_id}")
    connect.commit()
    connect.close()

def set_version(user_id: int, version:float):
    connect = sqlite3.connect("user.db")
    cursor = connect.cursor()
    cursor.execute(f"UPDATE user SET version = '{version}' WHERE id = {user_id}")
    connect.commit()
    connect.close()

def get_version(user_id: int):
    connect = sqlite3.connect("user.db")
    cursor = connect.cursor()
    cursor.execute(f"SELECT version FROM user WHERE id = {user_id}")
    version = float(str(cursor.fetchone())[1:-2])
    connect.close()
    return version
