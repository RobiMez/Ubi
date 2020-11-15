''' Connection testing tools '''

import asyncio
from telethon import events
from datetime import datetime
import time


@ubot.on(events.NewMessage(pattern=r"\.time", outgoing=True))  # pylint: disable=E0602
async def _(event):
    if event.fwd_from:
        return

    await event.edit(f"{time.ctime()}")
