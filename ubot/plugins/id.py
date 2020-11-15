from telethon import events
import pprint
from telethon.utils import pack_bot_file_id


async def _(event):
    sender = await event.get_input_sender()
    print(sender)


@ubot.on(events.NewMessage(pattern=r"\.id ?(.*)", outgoing=True))  # pylint: disable=E0602
async def _(event):
    # if forwarded message
    print(event)

    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    a_msg = ""
    if input_str:
        try:
            chat = await ubot.get_entity(input_str)  # pylint: disable=E0602
        except Exception as e:
            await event.edit(str(e))
            return None
        else:
            a_msg = f"{input_str} Chat ID: `{str(chat.id)}`\n"
    if event.reply_to_msg_id:
        r_msg = await event.get_reply_message()
        if r_msg.media:
            bot_api_file_id = pack_bot_file_id(r_msg.media)
            await event.edit("{}The BOT API file ID of this media is `{}`".format(a_msg, str(bot_api_file_id)))
        else:
            chat = await event.get_input_chat()
            await event.edit(f"""
current Chat_ID is `{str(event.chat_id)}` \n
User_ID: `{str(r_msg.from_id)}`
                            """)
    else:
        chat = await event.get_input_chat()
        await event.edit("{}The current chat's ID is `{}`!".format(a_msg, str(event.chat_id)))
