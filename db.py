import sqlite3
import os


def get_name_coin(value: int):
    if value % 10 in [2, 3, 4]:
        name_coin = "а"
    elif value % 10 in [5, 6, 7, 8, 9, 0]:
        name_coin = "ов"
    else:
        name_coin = ""
    return name_coin


# получить все значения из базы данных
def get_all_from_db(file_name: str, func: str, value_name: str, table_name=None):
    if table_name is None:
        table_name = file_name
    cur_dir = os.path.dirname(__file__)
    new_dir =os.path.relpath(f'..\\data\\{file_name}.db', cur_dir)
    connect = sqlite3.connect(new_dir)
    cursor = connect.cursor()
    cursor.execute(f"SELECT {func}{value_name} FROM {table_name}")
    value = cursor.fetchall()
    connect.close()
    return list(value)


# получить одно значение из базы данных
def get_from_db(file_name: str, value_name: str, user_id: int, table_name=None):
    if table_name is None:
        table_name = file_name
    cur_dir = os.path.dirname(__file__)
    new_dir = os.path.relpath(f'..\\data\\{file_name}.db', cur_dir)
    connect = sqlite3.connect(new_dir)
    cursor = connect.cursor()
    cursor.execute(f"SELECT {value_name} FROM {table_name} WHERE id = {user_id}")  # id const
    value = cursor.fetchone()[0]
    connect.close()
    return str(value)


# обновить значение в базе данных
def set_in_db(file_name: str, value_name: str, value: str, user_id: int, table_name=None):
    if table_name is None:
        table_name = file_name
    cur_dir = os.path.dirname(__file__)
    new_dir = os.path.relpath(f'..\\data\\{file_name}.db', cur_dir)
    connect = sqlite3.connect(new_dir)
    cursor = connect.cursor()
    cursor.execute(f"UPDATE {table_name} SET {value_name} = '{value}' WHERE id = {user_id}")  # id const
    connect.commit()
    connect.close()


# добавить значение в базу данных
def add_in_db(file_name: str, value_name: str, value: str, table_name=None):
    if table_name is None:
        table_name = file_name
    cur_dir = os.path.dirname(__file__)
    new_dir = os.path.relpath(f'..\\data\\{file_name}.db', cur_dir)
    connect = sqlite3.connect(new_dir)
    cursor = connect.cursor()
    try:
        cursor.execute(f"INSERT INTO {table_name} ({value_name}) VALUES ({value})")
    except sqlite3.IntegrityError:
        pass
    connect.commit()
    connect.close()
