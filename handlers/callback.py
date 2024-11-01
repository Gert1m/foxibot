from event.attack import logs
from upgrade.crit import crit
from upgrade.damage import damage
from upgrade.defence import defence
from upgrade.upgrade import upgrade


async def any_callback(call):
    callback = str(call.data)
    if callback.count("logs") != 0:
        await logs(call)
    elif callback.count("upgrade") != 0:
        await upgrade(call)
    elif callback.count("damage_up_info") != 0:
        await damage(call)
    elif callback.count("vision_up_info") != 0:
        await defence(call)
    elif callback.count("crit_uo_info") != 0:
        await crit(call)
