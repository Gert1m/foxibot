from datetime import datetime
from db import *


async def farm(message):
    user_id = message.from_user.id
    # фарм раз в день
    if datetime.toordinal(datetime.now()) > int(get_from_db("trade", "farm_time", user_id)):
        my_bank = int(get_from_db("trade", "bank", user_id))
        coefficient = int(float(get_from_db("trade", "coefficient", user_id)) * 100) / 100
        isVip = int(get_from_db("user", "isVip", user_id))
        farm_value = int(my_bank * coefficient / 100 + my_bank)
        max_bank_size = 5000 * 2 if isVip != 0 else 5000 * 1.5

        if farm_value > max_bank_size:  # проверка, что банк после фарма не превышает х2 от физического размера
            farm_value = max_bank_size

        set_in_db("trade", "bank", f"{farm_value}", user_id)

        coefficient = int(float(get_from_db("trade", "coefficient", -1)) * 100) / 100

        set_in_db("trade", "coefficient", f"{coefficient}", user_id)  # обновляем коэффициент пользователя
        set_in_db("trade", "farm_time", f"{datetime.toordinal(datetime.now())}", user_id)
