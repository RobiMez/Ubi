# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
""" This guy handles the loading/ unloading from telegram """
import asyncio
import os
import traceback
from ubot import util
from datetime import datetime


DELETE_TIMEOUT = 10


@ubot.on(util.admin_cmd(r"^\.load (?P<shortname>\w+)$"))
async def load_reload(event):
    await event.delete()
    shortname = event.pattern_match["shortname"]
    try:
        if shortname in ubot._plugins:
            ubot.remove_plugin(shortname)
        ubot.load_plugin(shortname)
        msg = await event.respond(f"Successfully (re)loaded plugin {shortname}")
        await asyncio.sleep(DELETE_TIMEOUT)
        await msg.delete()
    except Exception as e:
        tb = traceback.format_exc()
        logger.warn(f"Failed to (re)load plugin {shortname}: {tb}")
        await event.respond(f"Failed to (re)load plugin {shortname}: {e}")


@ubot.on(util.admin_cmd(r"^\.(?:unload) (?P<shortname>\w+)$"))
async def remove(event):

    shortname = event.pattern_match["shortname"]
    if shortname == "_core":
        msg = await event.edit(f"█ ❌ Cant remove core plugin : {shortname} █")
    elif shortname in ubot._plugins:
        ubot.remove_plugin(shortname)
        msg = await event.edit(f" ✅ Removed plugin {shortname} ")
    else:
        msg = await event.edit(f" ⚠️ Plugin {shortname} is not loaded")
        # deletes the message after it is read
    await asyncio.sleep(DELETE_TIMEOUT)
    await msg.delete()
