''' Connection testing tools '''

import asyncio
from telethon import events
from datetime import datetime


@ubot.on(events.NewMessage(pattern=r"\.ping", outgoing=True))  # pylint: disable=E0602
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    await event.edit("Bonking...")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit(f" Bonk! : `{ms} ms`")
