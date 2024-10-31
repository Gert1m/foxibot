from event.attack import logs
from upgrade.crit import crit
from upgrade.damage import damage
from upgrade.defence import defence
from upgrade.upgrade import upgrade


async def any_callback(call):
    callback = call.data
    if callback == "logs":
        await logs(call)
    elif callback == "upgrade":
        await upgrade(call)
    elif callback == "damage_up_info":
        await damage(call)
    elif callback == "vision_up_info":
        await defence(call)
    elif callback == "crit_uo_info":
        await crit(call)
