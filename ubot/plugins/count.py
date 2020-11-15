"""   Telegram message Enumeration tools   """

import asyncio
from telethon import events
from datetime import datetime
from telethon.tl.types import User, Chat, Channel


@ubot.on(events.NewMessage(pattern=r"\.count", outgoing=True))  # pylint: disable=E0602
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    u = 0  # number of users
    g = 0  # number of basic groups
    c = 0  # number of super groups
    bc = 0  # number of channels
    b = 0  # number of bots
    async for d in ubot.iter_dialogs(limit=None):  # pylint: disable=E0602
        if d.is_user:
            if d.entity.bot:
                b += 1
            else:
                u += 1
        elif d.is_channel:
            if d.entity.broadcast:
                bc += 1
            else:
                c += 1
        elif d.is_group:
            g += 1
        else:
            logger.info(d.stringify())  # pylint: disable=E0602
    end = datetime.now()
    ms = (end - start).seconds
    await event.edit(
        f"""
----------------------
Users:{u}
Groups:{g}
Super Groups:{c}
Channels:{bc}
Bots:{b}
----------------------
Obtained in {ms} seconds.
----------------------
""")

# This just logs the id of the message object.


@ubot.on(events.NewMessage(pattern=r"\.num ?(.*)", outgoing=True))  # pylint: disable=E0602
async def _(event):
    numchat = event.message.id
    await event.edit(f" There are `{numchat}` Text messages here.")
