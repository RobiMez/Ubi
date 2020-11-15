''' Connection testing tools '''
import os
from github import Github
from datetime import datetime
from telethon import events
import asyncio
pat = os.getenv("GITHUB_PAT")
g = Github(pat)


@ubot.on(events.NewMessage(pattern=r"\.git", outgoing=True))  # pylint: disable=E0602
async def _(event):
    if event.fwd_from:
        return

    user = g.get_user()
    print(user.name)

    await event.edit(f"{dir(user)}")
