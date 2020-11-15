"""Enable Seen Counter in any message,
to know how many users have seen your message
Syntax: .fwd as reply to any message"""
from telethon import events


@ubot.on(events.NewMessage(pattern=r"\.fwd", outgoing=True))  # pylint: disable=E0602
async def _(event):
    if event.fwd_from:
        return
    if Config.PRIVATE_CHANNEL_BOT_API_ID is None:  # pylint: disable=E0602
        await event.edit("Please set the required environment variable `PRIVATE_CHANNEL_BOT_API_ID` for this plugin to work")
        return False
    try:
        e = await ubot.get_entity(int(Config.PRIVATE_CHANNEL_BOT_API_ID))  # pylint: disable=E0602
    except Exception as e:
        await event.edit(str(e))
    else:
        re_message = await event.get_reply_message()
        # https://t.me/telethonofftopic/78166
        fwd_message = await ubot.forward_messages(  # pylint: disable=E0602
            e,
            re_message,
            silent=True
        )
        await ubot.forward_messages(  # pylint: disable=E0602
            event.chat_id,
            fwd_message
        )
        await fwd_message.delete()
        await event.delete()
