import sqlite3


def get_name_coin(value: int):
    if value % 10 in [2, 3, 4]:
        name_coin = "а"
    elif value % 10 in [5, 6, 7, 8, 9, 0]:
        name_coin = "ов"
    else:
        name_coin = ""
    return name_coin


def get_all_from_db(file_name: str, func: str, value_name: str):
    connect = sqlite3.connect(f"{file_name}.db")
    cursor = connect.cursor()
    table_name_in_file = file_name
    cursor.execute(f"SELECT {func}{value_name} FROM {table_name_in_file}")
    value = cursor.fetchall()
    connect.close()
    return list(value)


def get_from_db(file_name: str, value_name: str, user_id: int):
    connect = sqlite3.connect(f"{file_name}.db")
    cursor = connect.cursor()
    table_name_in_file = file_name
    cursor.execute(f"SELECT {value_name} FROM {table_name_in_file} WHERE id = {user_id}")  # id const
    value = cursor.fetchone()[0]
    connect.close()
    return str(value)


def set_in_db(file_name: str, value_name: str, value: str, user_id: int):
    connect = sqlite3.connect(f"{file_name}.db")
    cursor = connect.cursor()
    table_name_in_file = file_name
    cursor.execute(f"UPDATE {table_name_in_file} SET {value_name} = '{value}' WHERE id = {user_id}")  # id const
    connect.commit()
    connect.close()


def add_in_db(file_name: str, value_name: str, value: str):
    connect = sqlite3.connect(f"{file_name}.db")
    cursor = connect.cursor()
    table_name_in_file = file_name
    try:
        cursor.execute(f"INSERT INTO {table_name_in_file} ({value_name}) VALUES ({value})")
    except:
        pass
    connect.commit()
    connect.close()
