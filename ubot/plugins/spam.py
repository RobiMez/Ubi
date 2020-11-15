from telethon import events, errors


@ubot.on(events.NewMessage(pattern="\.spam (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Initializing spam ...")
    str = event.pattern_match.group(1)
    try:
        while True:
            await event.respond(f" {str}")
    except errors.MessageTooLongError as e:
        await event.respond(f"{e}")
